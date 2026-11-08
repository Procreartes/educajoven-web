#!/usr/bin/env python3
"""Genera la web de la Asociación Educajoven (educajoven.org), centrada en NOA (Noches Alternativas).

Uso:  python3 scripts/generar.py
Datos editables (Gestor de webs del portal o a mano): data/noa.json, data/jornadas.json
No edites los .html a mano: se sobrescriben.
"""
import datetime
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from web import RAIZ, Sitio, ICO, esc, datos, mailto  # noqa: E402

CORREO = "hola@educajoven.org"

S = Sitio(
    nombre="Asociación Educajoven", nombre_corto="Educajoven",
    dominio="https://educajoven.org",
    titular="Asociación Educajoven", nif="G10613016",
    domicilio="C/ Pi y Margall, 64 - 5.º B · 35006 Las Palmas de Gran Canaria",
    correo=CORREO, correo_datos="protecciondatos@educajoven.org",
    objeto="Esta web informa sobre la Asociación Educajoven y sus proyectos para la juventud, en especial NOA (Noches Alternativas), y sobre la forma de contactar.",
    color_tema="#0f1330", color_fondo="#0f1330",
    precarga=["unbounded-latin-800-normal.woff2", "dm-sans-latin-400-normal.woff2"],
    menu=[("/#noa", "NOA"), ("/#formatos", "Formatos"), ("/#donde", "Dónde"), ("/#jornadas", "Jornadas"),
          ("/#sumate", "Súmate"), ("/#asociacion", "La asociación")],
    marca='<span class="logo"><span class="logo-educa">educa</span><span class="logo-joven">joven</span></span>',
    pie_html='''<div class="pie-arriba">
      <div><p class="pie-logo"><span class="logo-educa">educa</span><span class="logo-joven">joven</span></p>
      <p>Asociación sin ánimo de lucro · Gran Canaria</p></div>
      <div><p><a href="mailto:hola@educajoven.org">hola@educajoven.org</a></p>
      <p class="pie-nota">NOA es un proyecto subvencionado por la Consejería de Educación y Juventud del Cabildo de Gran Canaria.</p></div>
    </div>''',
)

NOA = (datos("noa.json", []) or [{}])[0]
HOY = datetime.date.today().isoformat()
JORNADAS = sorted((j for j in datos("jornadas.json", []) if (j.get("fecha") or "") >= HOY),
                  key=lambda j: (j.get("fecha", ""), j.get("hora", "")))

FORMATOS = [
    ("Barrio", "Jornadas de proximidad en los barrios, en instalaciones municipales cedidas. Grupos de unas 30 personas.", "barrio"),
    ("Cumbre y Medianías", "Jornadas en núcleos dispersos como Tejeda o Temisas, con transporte para quienes participan y montaje en espacios sin equipamiento.", "cumbre"),
    ("Gran Formato", "Eventos de carácter insular con unas 160 personas, artistas, técnica y experiencias que no se pueden vivir en otro contexto. Con inscripción previa.", "gran"),
]

PILARES = [
    ("Actividades participativas", "Deporte, cultura, arte, formación y ocio, planificadas cada trimestre con un grupo motor de jóvenes que propone, organiza y evalúa."),
    ("Prevención", "Cada jornada es una alternativa al consumo de alcohol y otras drogas en los momentos de mayor riesgo, y muchas incluyen dinámicas y debate sobre ello."),
    ("Empleo juvenil", "El equipo de NOA se forma sobre todo con gente joven, y para muchas personas es su primera experiencia laboral."),
    ("Prácticas y voluntariado", "Acogemos alumnado en prácticas de ciclos formativos del ámbito sociocultural y deportivo, y formamos voluntariado y mediadores juveniles."),
]

LUGARES = [
    ("Agüimes", "Temisas, Cruce de Arinaga, Arinaga y el casco"),
    ("Santa Lucía de Tirajana", "Recursos juveniles e instalaciones municipales"),
    ("Ingenio y Teror", "Recursos juveniles e instalaciones municipales"),
    ("Tejeda", "Y otros núcleos de medianías y cumbre"),
]

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def fecha_larga(iso):
    try:
        d = datetime.date.fromisoformat(iso)
        return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]}"
    except (ValueError, TypeError):
        return iso or ""


def cielo():
    estrellas = [(8, 18, 1.4), (17, 64, 1), (26, 30, 1.8), (35, 80, 1.1), (44, 12, 1.2), (52, 52, 1.6), (61, 26, 1),
                 (70, 70, 1.3), (79, 40, 1.9), (88, 14, 1.1), (94, 58, 1.4), (12, 88, 1), (57, 90, 1.2), (83, 86, 1)]
    pts = "".join(f'<circle cx="{x}%" cy="{y}%" r="{r}"/>' for x, y, r in estrellas)
    return f'<svg class="cielo" aria-hidden="true" focusable="false">{pts}</svg>'


def jornadas_html():
    if not JORNADAS:
        return f'<p class="sin-jornadas">{esc(NOA.get("aviso") or "Las próximas jornadas se publicarán aquí muy pronto.")}</p>'
    filas = ""
    for j in JORNADAS:
        ins = j.get("inscripcion") or ""
        filas += f'''<li class="jornada">
      <div class="jornada-fecha"><strong>{esc(fecha_larga(j.get("fecha")))}</strong>{f'<span>{esc(j["hora"])}</span>' if j.get("hora") else ""}</div>
      <div class="jornada-info"><h3>{esc(j.get("titulo") or "Jornada NOA")}</h3>
        <p>{ICO["pin"]}<span>{esc(", ".join(x for x in [j.get("lugar"), j.get("municipio")] if x))}</span></p>
        {f'<span class="etiqueta">{esc(j["formato"])}</span>' if j.get("formato") else ""}</div>
      {f'<a class="boton boton-luz" href="{esc(ins)}" rel="noopener">Inscribirse {ICO["flecha"]}</a>' if ins.startswith("https://") else ""}
    </li>'''
    return f'<ol class="jornadas">{filas}</ol>'


def inicio():
    formatos = "".join(f'''<article class="formato formato-{k} aparece"><span class="formato-luna" aria-hidden="true"></span>
      <h3>NOA {esc(t)}</h3><p>{esc(d)}</p></article>''' for t, d, k in FORMATOS)
    pilares = "".join(f'<li class="aparece"><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in PILARES)
    lugares = "".join(f"<li><strong>{esc(m)}</strong><span>{esc(d)}</span></li>" for m, d in LUGARES)
    edicion = esc(NOA.get("edicion") or "")
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "NGO", "name": "Asociación Educajoven", "url": S.dominio + "/",
        "email": CORREO, "taxID": "G10613016", "areaServed": "Gran Canaria",
        "address": {"@type": "PostalAddress", "streetAddress": "C/ Pi y Margall, 64", "postalCode": "35006",
                    "addressLocality": "Las Palmas de Gran Canaria", "addressCountry": "ES"},
    }, ensure_ascii=False)

    cuerpo = f'''<section class="portada" id="noa">
  {cielo()}
  <div class="contenedor portada-grid">
    <div>
      <p class="antetitulo">Asociación Educajoven presenta{" · " + edicion if edicion else ""}</p>
      <h1><span class="noa">NOA</span><span class="noa-sub">Noches Alternativas</span></h1>
      <p class="entradilla">Ocio nocturno saludable, gratuito y participativo para la juventud de Gran Canaria. Viernes y sábados por la tarde-noche, en tu barrio, en la cumbre o a lo grande.</p>
      <div class="botones">
        <a class="boton boton-luz" href="#jornadas">Próximas jornadas {ICO["flecha"]}</a>
        <a class="boton boton-linea" href="#sumate">Súmate</a>
      </div>
    </div>
    <ul class="datos-noa" aria-label="NOA en breve">
      <li><strong>12 a 30</strong><span>años</span></li>
      <li><strong>19:00 – 02:00</strong><span>aproximadamente, viernes y sábados</span></li>
      <li><strong>Gratis</strong><span>acceso libre hasta completar aforo</span></li>
    </ul>
  </div>
  <div class="luna" aria-hidden="true"></div>
</section>

<section class="seccion" aria-labelledby="t-que">
  <div class="contenedor que-grid">
    <div><p class="antetitulo">Qué es NOA</p><h2 id="t-que">Un plan para el fin de semana que no depende de dónde vivas</h2></div>
    <div>
      <p class="entradilla">NOA abre las instalaciones públicas por la noche y las llena de actividades: deporte, cultura, arte, talleres y ocio. Hecho por jóvenes, para jóvenes y con jóvenes.</p>
      <p>Pensamos sobre todo en quien vive en barrios alejados, en zonas rurales o en la cumbre, y lo tiene difícil para acceder al ocio del fin de semana por dinero o por transporte. Por eso NOA va a donde está la gente y, cuando hace falta, pone la guagua.</p>
    </div>
  </div>
</section>

<section class="seccion seccion-alta" id="formatos" aria-labelledby="t-formatos">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Formatos</p><h2 id="t-formatos">Tres maneras de vivir la noche</h2></div>
    <div class="formatos">{formatos}</div>
  </div>
</section>

<section class="seccion" aria-labelledby="t-pilares">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Cómo funciona</p><h2 id="t-pilares">Cuatro pilares</h2></div>
    <ul class="pilares">{pilares}</ul>
  </div>
</section>

<section class="seccion seccion-alta" id="donde" aria-labelledby="t-donde">
  <div class="contenedor donde-grid">
    <div><p class="antetitulo">Dónde</p><h2 id="t-donde">Por toda la isla</h2>
    <p>NOA se desarrolla en canchas, pabellones, casas de la cultura, locales sociales, espacios jóvenes y patios de centros educativos fuera del horario lectivo, gracias a la colaboración de los ayuntamientos.</p>
    <p>¿Su municipio quiere sumarse? <a href="{mailto(CORREO, "Mi municipio quiere sumarse a NOA")}">Escríbannos</a>.</p></div>
    <ul class="lugares">{lugares}</ul>
  </div>
</section>

<section class="seccion" id="jornadas" aria-labelledby="t-jornadas">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Agenda</p><h2 id="t-jornadas">Próximas jornadas</h2>
    <p>Las actividades son gratuitas y de acceso libre hasta completar aforo. En las jornadas de Gran Formato, en las que tienen transporte o plazas limitadas, hay inscripción previa. Las personas menores de edad necesitan la autorización de su madre, su padre o su tutor legal.</p></div>
    {jornadas_html()}
  </div>
</section>

<section class="seccion seccion-alta" id="sumate" aria-labelledby="t-sumate">
  <div class="contenedor sumate">
    <div><p class="antetitulo">Súmate</p><h2 id="t-sumate">NOA lo deciden también quienes vienen</h2></div>
    <ul class="sumate-lista">
      <li><h3>Grupo motor</h3><p>Propón actividades, ayuda a organizarlas y evalúa con el equipo cómo ha ido cada trimestre.</p>
        <a href="{mailto(CORREO, "Quiero entrar en el grupo motor de NOA")}">Quiero entrar {ICO["flecha"]}</a></li>
      <li><h3>Voluntariado</h3><p>Fórmate como voluntario o mediador juvenil y colabora en las jornadas.</p>
        <a href="{mailto(CORREO, "Quiero hacer voluntariado en NOA")}">Quiero colaborar {ICO["flecha"]}</a></li>
      <li><h3>Prácticas</h3><p>Si estudias un ciclo del ámbito sociocultural o deportivo, puedes hacer tus prácticas en NOA.</p>
        <a href="{mailto(CORREO, "Prácticas en NOA")}">Más información {ICO["flecha"]}</a></li>
    </ul>
  </div>
</section>

<section class="seccion" id="asociacion" aria-labelledby="t-asoc">
  <div class="contenedor estrecho asociacion">
    <p class="antetitulo">La asociación</p>
    <h2 id="t-asoc">Asociación Educajoven</h2>
    <p class="entradilla">Somos una asociación sin ánimo de lucro de Gran Canaria que trabaja con y para la juventud: ocio saludable, participación, prevención, formación y empleo.</p>
    <p>NOA cuenta desde 2022 con el apoyo de la Consejería de Educación y Juventud del Cabildo de Gran Canaria, y con la colaboración de los ayuntamientos y centros educativos de los municipios donde se desarrolla.</p>
    <a class="boton boton-luz" href="mailto:{CORREO}">{ICO["mail"]} {CORREO}</a>
  </div>
</section>'''
    return S.pagina("NOA · Noches Alternativas · Asociación Educajoven",
                    "NOA: ocio nocturno saludable, gratuito y participativo para jóvenes de 12 a 30 años en Gran Canaria. Un proyecto de la Asociación Educajoven.",
                    "/", cuerpo, actual="", ld=ld)


def main():
    css = (RAIZ / "css/base.css").read_text(encoding="utf-8") + "\n" + (RAIZ / "css/tema.css").read_text(encoding="utf-8")
    S.escribir("css/estilos.css", css)
    S.publicar({"index.html": inicio()})


if __name__ == "__main__":
    main()
