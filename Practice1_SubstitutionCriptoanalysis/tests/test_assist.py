import assist

CRYPTOGRAM = """QATNT YSMHQ XJOCY HKATM FSNQI TUTMP TKTIP JIDTT KHIGQ ATCEG
JMHQA FNTYM TQRTY CSNTJ IEXQA TDTXY CIRTY ACIGT PVATI HQHNY
JFKMJ FHNTP"""

def test_report_runs_without_crashing():
    result = assist.report(CRYPTOGRAM, "en")
    assert isinstance(result, str)
    assert len(result) > 0


def test_report_matches_the_cryptogram_stats_from_the_handout():
    text = assist.eliminate_blanks(CRYPTOGRAM)
    assert len(text) == 110                 

    distinct_letters = set(text)
    assert len(distinct_letters) == 22


def test_report_rejects_unknown_language():
    import pytest
    with pytest.raises(ValueError):
        assist.report(CRYPTOGRAM, "fr")