xquery version "3.1";

declare option exist:serialize "method=xml";

<conservation_status>
{
    for $animal in //animal
    let $stat := //conservation_statistic[@animalid = $animal/@id]
    let $zoo := //zoo[@id = $animal/@zooid]
    return
        <animal>
            <name>{data($animal/name)}</name>
            <status>{data($stat/status)}</status>
            <population_in_wild>{data($stat/population_in_wild)}</population_in_wild>
            <population_in_captivity>{data($stat/population_in_captivity)}</population_in_captivity>
            <zoo>{data($zoo/name)}</zoo>
        </animal>
}
</conservation_status>
