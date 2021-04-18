# hason

## Examples

Lambda-calculus:

```
λ x. e ≡  {"": [["x"], "e"]}

f $ a ≡ ["f", "a"]
```

Literal:

```
[1, 2. 3] ≡ ["lit", [1, 2, 3]]
```

Let:

```json
{
  "x": 5,
  "": [["y"], ["+", "x", "y"]]
}
```

Recursive function:

```json
{
  "": [["x"], ["", "x"]]
}
```

Named functions, composition:

```json
{
  "f": {
    "": [["x"], "e"]
  },
  "g": {
    "": [["x"], "e2"]
  },
  ".": {
    "": [["f", "g"], ["f", ["g"]]]
  },
  "fg": [".", "f", "g"]
}
```

Debug print:

```json
{
  "": [[], "print", ["lit", "Hello, world!"]]
}
```

Serialization / deserialization:

```json
{
  "": [[], "print", ["serialize", ["lit", [1, 2]]], ["deserialize", ["lit","[1, 2]"]]]
}
```
