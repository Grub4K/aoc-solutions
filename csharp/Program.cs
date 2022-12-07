using AoCSolutions;

Dictionary<string, Dictionary<string, IAoCDay>> Lookup =
    new()
    {
        {
            "2022",
            new()
            {
                { "04", new AoCSolutions.Year2022.Day04() },
                { "05", new AoCSolutions.Year2022.Day05() },
            }
        },
    };

if (args.Length < 3)
{
    Console.Error.WriteLine("Expected exactly three arguments");
    return;
}
var year = args[0];
var day = args[1];
var path = args[2];

if (!Lookup.TryGetValue(year, out var yearLookup) || !yearLookup.TryGetValue(day, out var runner))
{
    Console.Error.WriteLine("This day is not (yet?) implemented");
    return;
}

try
{
    var results = runner.Run(path);
    if (results.Item1 is not null)
        Console.WriteLine($"{year}-{day} a: {results.Item1}");
    if (results.Item2 is not null)
        Console.WriteLine($"{year}-{day} b: {results.Item2}");
}
catch (Exception exception)
{
    Console.Error.WriteLine(
        exception switch
        {
            // TODO: Add all relevant Exceptions
            FileNotFoundException error => $"Input file not found: \"{error.FileName}\"",
            _ => exception,
        }
    );
}
