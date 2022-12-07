namespace AoCSolutions.Year2022;

using Line = ValueTuple<Range, Range>;

public record struct Range(byte Start, byte Stop);

class Day04 : AoCRunner<IEnumerable<Line>>, IAoCDay
{
    public override (object?, object?) Run(IEnumerable<Line> data)
    {
        var countSubset = 0;
        var countIntersection = 0;

        foreach (var (a, b) in data)
        {
            if (a.Start <= b.Start && b.Stop <= a.Stop || b.Start <= a.Start && a.Stop <= b.Stop)
                countSubset++;

            if (b.Start <= a.Stop && a.Start <= b.Stop || a.Start <= b.Stop && b.Start <= a.Stop)
                countIntersection++;
        }

        return (countSubset, countIntersection);
    }

    public override IEnumerable<Line> Process(IEnumerable<string> data) => data.Select(ProcessLine);

    public Line ProcessLine(string line)
    {
        var tokens = line.Split(',', count: 2);
        return (GetRange(tokens[0]), GetRange(tokens[1]));
    }

    public static Range GetRange(string range)
    {
        var tokens = range.Split('-', count: 2);
        var start = byte.Parse(tokens[0]);
        var stop = byte.Parse(tokens[1]);

        return new Range(start, stop);
    }
}
