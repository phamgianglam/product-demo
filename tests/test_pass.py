import pytest


@pytest.mark.asyncio
async def test_pass(reset_database):
    assert True
