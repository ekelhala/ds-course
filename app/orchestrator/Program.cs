
var builder = WebApplication.CreateBuilder();
var app = builder.Build();

app.MapGet("/", () => {
    return "test";
});

app.Run();