namespace AoCSolutions.Year2022;
using Result = ValueTuple<List<string>, List<Movement>>;

public record struct Movement(byte Count, byte From, byte To);

public class Day05 : AoCRunner<Result>, IAoCDay
{
    public override (object?, object?) Run(Result data)
    {
        var (boxes, movements) = data;
        return (Work(boxes.ToList(), movements), Work(boxes, movements, reverse: false));
    }

    public static string Work(List<string> boxes, List<Movement> movements, bool reverse = true)
    {
        foreach (var movement in movements)
        {
            var append = boxes[movement.From][^movement.Count..];
            boxes[movement.To] += reverse ? String.Join("", append.Reverse()) : append;
            boxes[movement.From] = boxes[movement.From][..^movement.Count];
        }
        return String.Join("", boxes.Select(x => x[^1..]));
    }

    public override Result Process(IEnumerable<string> data)
    {
        var enumerator = data.GetEnumerator();
        List<string>? boxes = null;

        while (enumerator.MoveNext())
        {
            var boxLine = String.Join("", enumerator.Current.Skip(1).Step(4));
            boxes ??= Enumerable.Repeat("", boxLine.Length).ToList();

            if (boxLine.All(char.IsDigit))
            {
                enumerator.MoveNext();
                break;
            }

            foreach (var index in ..boxLine.Length)
            {
                var character = boxLine[index];
                if (character == ' ')
                    continue;

                boxes[index] = $"{character}{boxes[index]}";
            }
        }

        List<Movement> movements = new();

        while (enumerator.MoveNext())
        {
            var line = enumerator.Current.Split().Skip(1).Step(2).ToArray();
            movements.Add(
                new(
                    byte.Parse(line[0].ToString()),
                    (byte)(byte.Parse(line[1].ToString()) - 1),
                    (byte)(byte.Parse(line[2].ToString()) - 1)
                )
            );
        }

        return (boxes!, movements);
    }
}
