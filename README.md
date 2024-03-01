# Recipe Book

```sh
pip install -r requirements.txt
python3 backend/main.py

npm install
npm run dev

```


```text
/
├───backend
├───frontend
│   ├───public
│   └───src
│       ├───components
│       │   └───edit
│       ├───layouts
│       ├───lib
│       ├───pages
│       │   ├───edit
│       │   └───recipe
│       └───stores
├───mongodb
│   ├───mongo-config
│   └───mongo-data
└───public
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro/React/Vue/Svelte/Preact components.

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

