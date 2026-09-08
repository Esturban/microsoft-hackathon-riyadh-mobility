from pathlib import Path

INFRA_MAIN = Path(__file__).resolve().parents[1] / "infra" / "main.bicep"
MAPS_MODULE = Path(__file__).resolve().parents[1] / "infra" / "modules" / "maps.bicep"


def test_cosmos_account_name_stays_unique_and_within_azure_limit_for_long_environments():
    source = INFRA_MAIN.read_text()

    assert "var suffix = uniqueString(resourceGroup().id, envName)" in source
    assert "var cosmosEnvSlug = take(replace(envSlug, '-', ''), 7)" in source
    assert "var cosmosName = 'cosmos-rmd-${cosmosEnvSlug}-${suffix}'" in source
    assert len("cosmos-rmd-" + ("a" * 7) + "-" + ("b" * 13)) <= 44

    def cosmos_name(environment_slug: str, suffix: str) -> str:
        compact_slug = environment_slug.replace("-", "")[:7]
        return f"cosmos-rmd-{compact_slug}-{suffix}"

    assert cosmos_name("riyadh-urban-hackathon-wus2", "a" * 13) != cosmos_name(
        "riyadh-urban-hackathon-wus3", "b" * 13
    )


def test_azure_maps_account_is_declared_in_the_global_region():
    main_source = INFRA_MAIN.read_text()
    source = MAPS_MODULE.read_text()

    assert "param location string = 'global'" in source
    assert "location: location" in source
    assert "var mapsLocation = 'global'" in main_source
    assert "location: mapsLocation" in main_source
