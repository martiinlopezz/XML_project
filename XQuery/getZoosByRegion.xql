xquery version "3.1";

declare option exist:serialize "method=xml";

<zoos_by_region>
{
    for $region in distinct-values(//zoo/@location)
    return
        <region>
            <name>{data($region)}</name>
            <zoos>
            {
                for $zoo in //zoo[@location = $region]
                return
                    <zoo>
                        <name>{data($zoo/name)}</name>
                        <animals>
                        {
                            for $animal in //animal[@zooid = $zoo/@id]
                            return
                                <animal>
                                    <name>{data($animal/name)}</name>
                                    <diet>{data($animal/diet)}</diet>
                                </animal>
                        }
                        </animals>
                    </zoo>
            }
            </zoos>
        </region>
}
</zoos_by_region>
