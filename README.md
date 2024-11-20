# Blender Custom Mesh

I created this to make it easier to me to add custom meshes I created.

## Why

I don't know how to use Blender. I want to create some assets and easily import into my projects the most used ones.

### The code is ugly

I don't care. Probably I'll never touch it again, only to add menus and files.

## How to use

create a file ~/.config/custom_assets.json

``` json
{
    "menu": [
        {
            "label": "Example",
            "path": "~/models/pcb",
            "files": [
                {
                    "label": "Something",
                    "file": "example"
                }
            ]
        }
    ]
}
```

> Don't add '.blend' extension to files!

## Issues or suggestions?

Ping me on github.
