TEMPLATES = {
    "Web Vanilla": """mi-proyecto-vanilla/
├── public/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── assets/
│   ├── images/
│   └── fonts/
└── README.md""",

    "Express": """api-express/
├── app.js
├── package.json
├── routes/
│   ├── index.js
│   └── users.js
├── controllers/
│   └── usersController.js
├── models/
│   └── user.model.js
├── middleware/
└── .env""",

    "MVC": """mvc-proyecto/
├── config/
│   └── database.js
├── controllers/
│   └── userController.js
├── models/
│   └── userModel.js
├── views/
│   ├── layouts/
│   └── partials/
├── routes/
│   └── userRoutes.js
└── app.js""",

    "Hexagonal": """hexagonal-app/
├── adapters/
│   ├── infrastructure/
│   └── presentation/
├── application/
│   ├── usecases/
│   └── dtos/
├── domain/
│   ├── entities/
│   └── repositories/
├── interfaces/
└── config/
    └── database.js"""
}

DEFAULT_EXAMPLE = """mi-proyecto/
├── src/                   # Código fuente
│   ├── components/        # Componentes React
│   │   ├── Header.jsx     # Cabecera
│   │   └── Footer.jsx     # Pie de página
│   ├── pages/             # Páginas
│   │   ├── Home.jsx       # Página principal
│   │   └── About.jsx      # Acerca de
│   ├── utils/             # Utilidades
│   │   └── helpers.js     # Funciones auxiliares
│   └── App.jsx            # Componente principal
├── public/                # Archivos públicos
│   ├── index.html         # HTML base
│   ├── favicon.ico        # Icono
│   └── images/            # Imágenes
│       ├── logo.png       # Logo
│       └── banner.jpg     # Banner
├── docs/                  # Documentación
│   ├── README.md          # Documentación principal
│   └── API.md             # Documentación API
├── package.json           # Configuración npm
├── .gitignore             # Archivos ignorados por Git
└── LICENSE                # Licencia del proyecto"""