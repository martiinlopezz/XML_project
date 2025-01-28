xquery version "3.1";

declare option exist:serialize "method=xml";

<old_zoos>
{
    for $zoo in //zoo[xs:integer(foundation) < 1900]
    return
        <zoo>
            <name>{data($zoo/name)}</name>
            <city>{data($zoo/city)}</city>
            <foundation>{data($zoo/foundation)}</foundation>
        </zoo>
}
</old_zoos>
