namespace AoCSolutions;

public static class Extensions
{
    public static RangeEnumerator GetEnumerator(this Range range) => new(range);

    public static IEnumerable<T> Step<T>(this IEnumerable<T> enumerable, int step)
    {
        var enumerator = enumerable.GetEnumerator();
        var index = step;

        while (enumerator.MoveNext())
        {
            if (index == step)
            {
                index = 1;
                yield return enumerator.Current;
            }
            else
            {
                ++index;
            }
        }
    }

    public static string ToPrettyString<T>(this T[] array) =>
        $$"""{{typeof(T).Name}}[{{array.Length}}] { {{string.Join(", ", array)}} }""";

    public static string ToPrettyString<T>(this IList<T> list) =>
        $$"""IList<{{typeof(T).Name}}>({{list.Count}}) { {{string.Join(", ", list)}} }""";

    public static string ToPrettyString<T>(this IEnumerable<T> enumerable) =>
        $$"""IEnumerable<{{typeof(T).Name}}> { {{string.Join(", ", enumerable)}} }""";

    public static Dictionary<A, B> ToDictionary<A, B>(this IEnumerable<(A, B)> enumerable)
        where A : notnull => enumerable.ToDictionary(x => x.Item1, x => x.Item2);
}

public class RangeEnumerator
{
    public int Current { get; private set; }
    private readonly int End;
    private readonly bool Reversed;

    public RangeEnumerator(Range range)
    {
        Current = range.Start.IsFromEnd ? 0 : range.Start.Value;
        End = range.End.IsFromEnd ? int.MaxValue : range.End.Value;
        Reversed = Current > End;
        if (!Reversed)
            Current -= 1;
    }

    public bool MoveNext()
    {
        if (Reversed)
            --Current;
        else
            ++Current;

        return (Current < End) ^ Reversed;
    }

    public static implicit operator RangeEnumerator(Range range) => new(range);
}
