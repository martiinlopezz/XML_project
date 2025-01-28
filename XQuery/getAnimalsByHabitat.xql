xquery version "3.1";

declare option exist:serialize "method=xml";

<animals_by_habitat>
{
    for $habitat in distinct-values(//animal/habitat)
    return
        <habitat>
            <name>{data($habitat)}</name>
            <animals>
            {
                for $animal in //animal[habitat = $habitat]
                return
                    <animal>
                        <name>{data($animal/name)}</name>
                        <diet>{data($animal/diet)}</diet>
                    </animal>
            }
            </animals>
        </habitat>
}
</animals_by_habitat>
