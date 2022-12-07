namespace AoCSolutions;

public interface IAoCDay
{
    public (string?, string?) Run(string data);
}

public abstract class AoCRunner<T>
{
    public AoCRunner() { }

    public (string?, string?) Run(string path)
    {
        var value = Run(Process(Read(path)));
        return (value.Item1?.ToString(), value.Item2?.ToString());
    }

    public abstract (object?, object?) Run(T data);

    public IEnumerable<string> Read(string path)
    {
        using var file = File.OpenRead(path);
        using var stringReader = new StreamReader(file);

        string? line;
        while ((line = stringReader.ReadLine()) is not null)
            yield return line;
    }

    public abstract T Process(IEnumerable<string> data);
}

public abstract class AoCRunner : AoCRunner<IEnumerable<string>>
{
    public override IEnumerable<string> Process(IEnumerable<string> data) => data;
}
