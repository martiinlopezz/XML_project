xquery version "3.1";

declare option exist:serialize "method=xml";

<carnivores>
{
    for $animal in //animal[diet = 'Carnivore']
    let $zoo := //zoo[@id = $animal/@zooid]
    return
        <animal>
            <name>{data($animal/name)}</name>
            <habitat>{data($animal/habitat)}</habitat>
            <zoo>{data($zoo/name)}</zoo>
        </animal>
}
</carnivores>
