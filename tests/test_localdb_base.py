from pathlib import Path

import pytest

import esco

TESTDIR = Path(__file__).parent


@pytest.fixture
def db(tmpdir):
    yield esco.LocalDB()


def test_load_occupations(db):
    occupations = db.load_occupations()
    assert len(occupations) > 70


def test_load_skills(db):
    skills = db.load_skills()
    assert len(skills) > 800


def test_get_label(db):
    assert db
    assert db.get_label("esco:b0096dc5-2e2d-4bc1-8172-05bf486c3968")
    assert db.get_label(
        "http://data.europa.eu/esco/skill/b0096dc5-2e2d-4bc1-8172-05bf486c3968"
    )


def test_get_missing_return_none(db):
    assert db.get("esco:nonexistent") is None


def test_get_skill(db):
    skill = db.get("esco:b0096dc5-2e2d-4bc1-8172-05bf486c3968")
    assert skill["description"]
    assert skill["skillType"] == "skill"


@pytest.mark.parametrize(
    "products,expected_results",
    [({"ansible", "JBoss", "Bash"}, 3), ({"agile", "scrum", "kanban"}, 1)],
)
def test_search_skill_label(db, products, expected_results):
    skills = db.search_products(products)
    assert len(skills) >= expected_results
