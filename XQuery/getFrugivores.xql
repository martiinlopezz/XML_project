xquery version "3.1";

declare option exist:serialize "method=xml";

<frugivores>
{
    for $animal in //animal[diet = 'Frugivore']
    let $zoo := //zoo[@id = $animal/@zooid]
    return
        <animal>
            <name>{data($animal/name)}</name>
            <habitat>{data($animal/habitat)}</habitat>
            <zoo>
                <name>{data($zoo/name)}</name>
                <city>{data($zoo/city)}</city>
            </zoo>
        </animal>
}
</frugivores>
