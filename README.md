# PI_ML_OPS

## Todo
- **API EXAMPLE** https://api-pi-82r8.onrender.com/api/get_score_count?platform=amazon&year=2014&scored=3
- **[Front Page](https://spiffy-front.vercel.app)**

### Transformaciones

- [x] Generar campo id: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = as123)

- [x] Los valores nulos del campo rating deberán reemplazarse por el string “G” corresponde al maturity rating: “general for all audiences”

- [x] De haber fechas, deberán tener el formato AAAA-mm-dd

- [x] Los campos de texto deberán estar en minúsculas, sin excepciones

- [x] El campo duration debe convertirse en dos campos: duration_int y duration_type. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)

- [x] Dataset de ratings y plataformas subido a mongoDB despues de limpiarlos.
### API

- [x] Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type))

- [x] Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))

- [x] Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))

- [x] Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))

### Parametros:
- **platform**: amazon, hulu, disney, netflix
- **duration_type**: seasons, min
- **year**

### Ejemplos:

#### get_max_duration

*`/api/get_max_duration/?**platform**=amazon&**year**=2010&**duration_type**=seasons`*

#### get_count_platform

*`/api/get_count_platform/?**platform**=amazon`*

#### get_actor

*`/api/get_actor/?**platform**=amazon&**year**=2010`*

#### predict model

[Ir a la url del modelo](https://huggingface.co/printer130/ml/tree/main)

*`/api/predict/?user_id=500&title=the%20shadow%20of%20the%20sun`*

<br>

- [x] **`Análisis exploratorio de los datos: (Exploratory Data Analysis-EDA)`**:

- [x] **`Sistema de recomendación`**: 
