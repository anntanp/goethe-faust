"""
Purpose:    Unit tests for the transform package.
Usage:      pytest scripts/transform/tests/ -q
Deps:       pytest
Assumes:    Run from project root (goethe-faust/).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# ── Package import ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # adds scripts/ to sys.path

from transform.constants import GRAPH_MOCHO, MOCHO_NS, PROJECT_DIR
from transform.utils import (
    coerce_list,
    make_nq,
    mint_bare_id,
    mint_cho_uri,
    normalize_date,
    value_to_nt_obj,
    _escape_literal,
    get_object_id,
)
from transform.emitters import (
    retype_entities,
    emit_creator_triples,
    emit_contributor_triples,
    emit_subject_triples,
    emit_aggregation_triples,
    emit_place_stubs,
    werk_staging_row,
)
from transform.loaders import load_mediatype_class, load_htype_map

# Config table paths
_CONFIG = PROJECT_DIR / "output" / "config"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _rdf_types(lines: list[str]) -> set[str]:
    """Extract the object IRIs from all rdf:type triples in a list of N-Quads lines."""
    rdf_type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    result: set[str] = set()
    for line in lines:
        parts = line.split()
        if len(parts) >= 4 and f"<{rdf_type}>" in parts[1]:
            obj = parts[2].strip("<>")
            result.add(obj)
    return result


def _predicates(lines: list[str]) -> set[str]:
    result: set[str] = set()
    for line in lines:
        parts = line.split()
        if len(parts) >= 4:
            result.add(parts[1].strip("<>"))
    return result


def _load_configs():
    mc_map = load_mediatype_class(_CONFIG / "lookup_mediatype_class.csv")
    ht_map = load_htype_map(_CONFIG / "lookup_htype_doco_rico.csv")
    return mc_map, ht_map


# ── normalize_date ────────────────────────────────────────────────────────────

class TestNormalizeDate:
    def test_compact_yyyymmdd(self):
        assert normalize_date("19870315") == ["1987-03-15"]

    def test_iso_interval(self):
        result = normalize_date("1900/1950")
        assert result == ["1900", "1950"]

    def test_passthrough(self):
        assert normalize_date("ca. 1900") == ["ca. 1900"]

    def test_iso_already(self):
        assert normalize_date("2026-05-01") == ["2026-05-01"]


# ── mint_bare_id ──────────────────────────────────────────────────────────────

class TestMintBareId:
    _id = "A" * 32

    def test_providedcho_bare_id(self):
        result = mint_bare_id("ProvidedCHO", self._id)
        assert result == f"http://www.deutsche-digitale-bibliothek.de/item/{self._id}"

    def test_other_entity_bare_id(self):
        result = mint_bare_id("Agent", self._id)
        assert result == f"urn:ddbedm:Agent:{self._id}"

    def test_full_uri_passthrough(self):
        uri = "http://d-nb.info/gnd/1234567"
        assert mint_bare_id("Agent", uri) == uri

    def test_urn_passthrough(self):
        urn = "urn:ddbedm:Agent:12345"
        assert mint_bare_id("Agent", urn) == urn


# ── value_to_nt_obj ───────────────────────────────────────────────────────────

class TestValueToNtObj:
    def test_string(self):
        assert value_to_nt_obj("hello") == ['"hello"']

    def test_empty_string(self):
        assert value_to_nt_obj("") == []

    def test_none(self):
        assert value_to_nt_obj(None) == []

    def test_resource_dict(self):
        assert value_to_nt_obj({"resource": "http://example.org/"}) == ["<http://example.org/>"]

    def test_lang_dict(self):
        result = value_to_nt_obj({"$": "Faust", "lang": "de"})
        assert result == ['"Faust"@de']

    def test_no_lang_dict(self):
        result = value_to_nt_obj({"$": "Faust", "lang": None})
        assert result == ['"Faust"']

    def test_list_flattened(self):
        result = value_to_nt_obj([{"$": "A", "lang": "de"}, {"$": "B", "lang": "en"}])
        assert '"A"@de' in result and '"B"@en' in result

    def test_escape_quotes(self):
        result = value_to_nt_obj('say "hi"')
        assert result == ['"say \\"hi\\""']

    def test_escape_newlines(self):
        result = value_to_nt_obj("line1\nline2\r\nline3")
        assert result == ['"line1\\nline2\\r\\nline3"']


# ── get_object_id ─────────────────────────────────────────────────────────────

class TestGetObjectId:
    _id = "B" * 32

    def test_full_url(self):
        record = {"edm": {"RDF": {"ProvidedCHO": {"about": f"http://www.deutsche-digitale-bibliothek.de/item/{self._id}"}}}}
        assert get_object_id(record) == self._id

    def test_bare_id(self):
        record = {"edm": {"RDF": {"ProvidedCHO": {"about": self._id}}}}
        assert get_object_id(record) == self._id

    def test_missing_about(self):
        record = {"edm": {"RDF": {"ProvidedCHO": {}}}}
        assert get_object_id(record) is None

    def test_missing_cho(self):
        record = {"edm": {"RDF": {}}}
        assert get_object_id(record) is None


# ── retype_entities ───────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def configs():
    return _load_configs()


_SPARTE001 = "http://ddb.vocnet.org/sparte/sparte001"
_SPARTE002 = "http://ddb.vocnet.org/sparte/sparte002"
_SPARTE003 = "http://ddb.vocnet.org/sparte/sparte003"
_MT001     = "http://ddb.vocnet.org/medientyp/mt001"
_MT002     = "http://ddb.vocnet.org/medientyp/mt002"
_MT003     = "http://ddb.vocnet.org/medientyp/mt003"
_MT007     = "http://ddb.vocnet.org/medientyp/mt007"


class TestRetypeEntities:
    _cho_nt = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "C" * 32 + ">"

    def _call(self, sector, mediatype, htype, configs, dctype_vals=None):
        mc_map, ht_map = configs
        return retype_entities(
            sector, mediatype, htype, dctype_vals or [],
            self._cho_nt, mc_map, ht_map, {}, GRAPH_MOCHO,
        )

    def test_sparte004_mt003_no_htype_fallback(self, configs):
        """sparte004/mt003 use_htype=True; no htype → fixed M class rdac:C10007."""
        _SPARTE004 = "http://ddb.vocnet.org/sparte/sparte004"
        lines, target_class, wemi, _flags = self._call(_SPARTE004, _MT003, None, configs)
        types = _rdf_types(lines)
        assert "http://rdaregistry.info/Elements/c/C10007" in types
        assert wemi == "M"

    def test_sparte001_mt003_htype021(self, configs):
        """sparte001/mt003 use_htype=True; htype_021 → rdac:C10001+C10007 from htype, mocho:Manifestation added."""
        lines, target_class, wemi, _flags = self._call(_SPARTE001, _MT003, "htype_021", configs)
        types = _rdf_types(lines)
        assert "http://rdaregistry.info/Elements/c/C10001" in types
        assert "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#Manifestation" in types
        assert wemi == "W"

    def test_sparte003_mt001_fixed(self, configs):
        """sparte003/mt001 use_htype=False → mocho:ImmovableWork (W) + aco:AudioManifestation (M)."""
        lines, target_class, wemi, _flags = self._call(_SPARTE003, _MT001, None, configs)
        types = _rdf_types(lines)
        assert MOCHO_NS + "ImmovableWork" in types
        assert "https://w3id.org/ac-ontology/aco#AudioManifestation" in types

    def test_mt007_guard_does_not_add_types_here(self, configs):
        """retype_entities itself doesn't know about mt007; caller guards. Falls back to mocho:Manifestation."""
        lines, target_class, wemi, _flags = self._call(_SPARTE001, _MT007, None, configs)
        assert target_class != ""  # always returns something

    def test_unknown_sector_mediatype_fallback(self, configs):
        """Unknown (sector, mediatype) → ('any','any') D9 fallback mocho:Manifestation."""
        lines, target_class, wemi, _flags = self._call("any", "any", None, configs)
        types = _rdf_types(lines)
        assert MOCHO_NS + "Manifestation" in types
        assert target_class == MOCHO_NS + "Manifestation"


# ── emit_creator_triples ──────────────────────────────────────────────────────

class TestEmitCreatorTriples:
    _cho_nt = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "D" * 32 + ">"
    _agent_uri = "http://d-nb.info/gnd/118540238"
    _rdac_c10007 = "http://rdaregistry.info/Elements/c/C10007"
    _rdam_P30329 = "http://rdaregistry.info/Elements/m/P30329"

    def _agents_index(self):
        return {
            self._agent_uri: {
                "about":     self._agent_uri,
                "prefLabel": "Goethe, Johann Wolfgang von",
            }
        }

    def _align(self):
        """Minimal class_prop_align for rdac:C10007/dc:creator → rdam:P30329."""
        dc_creator = "http://purl.org/dc/elements/1.1/creator"
        return {(self._rdac_c10007, dc_creator): self._rdam_P30329}

    def test_track1_iri(self):
        vals = [{"resource": self._agent_uri, "$": "", "lang": ""}]
        lines = emit_creator_triples(
            self._cho_nt, vals, {}, self._rdac_c10007, self._align(), GRAPH_MOCHO,
        )
        preds = _predicates(lines)
        assert self._rdam_P30329 in preds

    def test_track2_agent_stub(self):
        vals = [{"resource": self._agent_uri, "$": "Goethe", "lang": ""}]
        lines = emit_creator_triples(
            self._cho_nt, vals, self._agents_index(), self._rdac_c10007,
            self._align(), GRAPH_MOCHO,
        )
        preds = _predicates(lines)
        assert "http://purl.org/dc/terms/creator" in preds
        assert "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in preds

    def test_label_only_no_track2(self):
        """Label-only creator: Track 2 is silent (no dcterms:creator without URI)."""
        vals = [{"resource": "", "$": "Unbekannt", "lang": "de"}]
        lines = emit_creator_triples(
            self._cho_nt, vals, {}, self._rdac_c10007, self._align(), GRAPH_MOCHO,
        )
        assert "http://purl.org/dc/terms/creator" not in _predicates(lines)
        assert self._rdam_P30329 in _predicates(lines)

    def test_no_match_no_crash(self):
        lines = emit_creator_triples(
            self._cho_nt, [], {}, self._rdac_c10007, {}, GRAPH_MOCHO,
        )
        assert lines == []


# ── emit_contributor_triples ──────────────────────────────────────────────────

class TestEmitContributorTriples:
    _cho_nt   = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "E" * 32 + ">"
    _agent_uri = "http://d-nb.info/gnd/987654321"
    _lido_creation = "http://terminology.lido-schema.org/lido00012"
    _rdac_c10007   = "http://rdaregistry.info/Elements/c/C10007"

    def test_lido_dispatch_matched(self):
        event_idx = {self._agent_uri: self._lido_creation}
        lido_row = {
            "rdam_agent_prop": "http://rdaregistry.info/Elements/m/P30329",
            "dc_agent_fallback": "http://purl.org/dc/elements/1.1/contributor",
        }
        lido_dispatch = {self._lido_creation: lido_row}
        vals = [{"resource": self._agent_uri, "$": "Schiller", "lang": ""}]
        lines = emit_contributor_triples(
            self._cho_nt, vals, event_idx, lido_dispatch,
            self._rdac_c10007, "M", GRAPH_MOCHO,
        )
        preds = _predicates(lines)
        assert "http://rdaregistry.info/Elements/m/P30329" in preds

    def test_no_event_fallback_dc_contributor(self):
        vals = [{"resource": self._agent_uri, "$": "X", "lang": ""}]
        lines = emit_contributor_triples(
            self._cho_nt, vals, {}, {}, self._rdac_c10007, "M", GRAPH_MOCHO,
        )
        preds = _predicates(lines)
        assert "http://purl.org/dc/elements/1.1/contributor" in preds

    def test_label_only_literal_fallback(self):
        vals = [{"resource": "", "$": "Anonym", "lang": "de"}]
        lines = emit_contributor_triples(
            self._cho_nt, vals, {}, {}, self._rdac_c10007, "M", GRAPH_MOCHO,
        )
        preds = _predicates(lines)
        assert "http://purl.org/dc/elements/1.1/contributor" in preds
        assert any('"Anonym"@de' in nq for nq in lines)


# ── emit_subject_triples ──────────────────────────────────────────────────────

class TestEmitSubjectTriples:
    _cho_nt = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "F" * 32 + ">"

    def test_iri_subject(self):
        vals = [{"resource": "http://d-nb.info/gnd/4018197-4", "$": "Faust", "lang": "de"}]
        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
        preds = _predicates(lines)
        assert "http://purl.org/dc/terms/subject" in preds

    def test_literal_subject(self):
        vals = [{"resource": "", "$": "Goethe", "lang": "de"}]
        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
        preds = _predicates(lines)
        assert "http://purl.org/dc/elements/1.1/subject" in preds

    def test_dedup(self):
        uri = "http://d-nb.info/gnd/4018197-4"
        vals = [
            {"resource": uri, "$": "Faust", "lang": "de"},
            {"resource": uri, "$": "Faust", "lang": "de"},
        ]
        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
        dcterms_sub_lines = [l for l in lines if "terms/subject" in l]
        assert len(dcterms_sub_lines) == 1


# ── emit_place_stubs ──────────────────────────────────────────────────────────

class TestEmitPlaceStubs:
    def test_emits_label(self):
        places = [{"about": "http://example.org/place/1",
                   "prefLabel": [{"$": "Weimar", "lang": "de"}]}]
        lines = emit_place_stubs(places, GRAPH_MOCHO)
        assert any('"Weimar"@de' in nq for nq in lines)

    def test_no_about_skipped(self):
        places = [{"prefLabel": [{"$": "Weimar", "lang": "de"}]}]
        lines = emit_place_stubs(places, GRAPH_MOCHO)
        assert lines == []

    def test_none_input(self):
        assert emit_place_stubs(None, GRAPH_MOCHO) == []


# ── werk_staging_row ──────────────────────────────────────────────────────────

class TestWerkStagingRow:
    _cho_uri = "https://gemea.ise.fiz-karlsruhe.de/mocho/" + "G" * 32
    _rdac_c10001 = "http://rdaregistry.info/Elements/c/C10001"
    _rdac_c10007 = "http://rdaregistry.info/Elements/c/C10007"

    def test_w_slot_returns_row(self):
        cho = {"title": {"$": "Faust", "lang": "de"},
               "creator": [{"resource": "http://d-nb.info/gnd/118540238", "$": "Goethe"}]}
        row = werk_staging_row(self._cho_uri, cho, self._rdac_c10001)
        assert row is not None
        assert row["dc_title"] == "Faust"
        assert "http://d-nb.info/gnd/118540238" in row["creator_uris"]

    def test_m_slot_returns_none(self):
        cho = {"title": {"$": "Faust"}}
        row = werk_staging_row(self._cho_uri, cho, self._rdac_c10007)
        assert row is None

    def test_obj_id_extracted(self):
        cho = {}
        row = werk_staging_row(self._cho_uri, cho, self._rdac_c10001)
        assert row["ddb_obj_id"] == "G" * 32


# ── make_nq ───────────────────────────────────────────────────────────────────

def test_make_nq_format():
    line = make_nq("<http://s>", "<http://p>", '"o"', "https://graph/g")
    assert line == '<http://s> <http://p> "o" <https://graph/g> .'
