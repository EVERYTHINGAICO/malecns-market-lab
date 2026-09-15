# Protocolo experimental: MaleCNS/fly.ai frente al sistema de referencia

**Estado: plan prerregistrable; evaluación no ejecutada.** No hay resultados financieros ni evidencia OOS que permita integrar MaleCNS. Decisión actual: **NEED MORE DATA**. El propósito es intentar refutar su utilidad, con el mismo rigor que se exigiría para aceptarla.

Este documento y `../protocol.json` son el plan de trabajo para un modelo económico. Los valores todavía `null` representan información que debe fijarse antes de ejecutar o abrir el test; no autorizan al ejecutor a inventarla. Todo el trabajo irá en una carpeta aislada. No se modificará el bot, no se leerán claves y no se conectará trading real.

## 1. Qué se ha comprobado y qué falta

La implementación candidata es [alextitonis/fly.ai](https://github.com/alextitonis/fly.ai), fijada al commit **0aa078055f7a975075ba5baf1156430f9e606356**. Su documentación describe un reservoir basado en MaleCNS, con dinámica neuronal fija y readout externo. El [proyecto MaleCNS de Janelia](https://male-cns.janelia.org/) publica el connectoma; eso no es evidencia de capacidad financiera.

Se inspeccionaron, sin ejecutarlos, `flybrain/brain.py` y `flybrain/reservoir.py` del commit indicado. Hay una advertencia concreta: **`folds()` usa k-fold o leave-one-group-out, que pueden entrenar con observaciones posteriores a las que validan**. No utilizar `Readout.fit()` con esa validación por defecto para series financieras. PCA se ajusta dentro de sus folds, pero los folds no garantizan causalidad temporal. Su readout logístico es binario, por lo que no se debe fingir que entrega directamente tres clases. Ver [código fijado](https://github.com/alextitonis/fly.ai/blob/0aa078055f7a975075ba5baf1156430f9e606356/flybrain/reservoir.py). No se incluye código upstream ni se descargó el connectoma completo.

El prototipo de observación de señales actual registra avisos/señales y compras rivales. **No es un simulador de fills ni PnL** y no sustituye al sistema A. Sus registros sirven para disponibilidad temporal y latencia, no para llamar ganadoras a las operaciones. Las muestras previas elegidas entre compras rivales tampoco constituyen un universo imparcial para entrenar.

### Bloqueos que hay que resolver antes de medir alpha

1. **A exacto:** identificar el código realmente ejecutado y su configuración efectiva, no solo una copia de `STATE.md`. Obtener un snapshot en lectura, hash/commit, dependencias y estado inicial. Puede haber cambios de otro agente; jamás editar su checkout para este experimento.
2. **Shorts:** en el contexto actual Pons se opera al contado. Vender inventario no es abrir un SHORT. No se ha verificado un instrumento vendible en corto, préstamo ni costes asociados. Predicción SHORT se puede evaluar como dirección bajista, pero **su PnL ejecutable será N/A** mientras no exista una ruta real. No trasladar C a futuros y comparar contra A en spot. Una evaluación long/short completa exigiría un experimento separado con idénticos instrumentos accesibles a todos.
3. **Historia causal:** demostrar disponibilidad de universo, trades, reservas, comisiones, distribuidores y épocas. Un estado `latest` no reconstruye el pasado. Si faltan trazas o datos económicos necesarios, recolectar prospectivamente sin fingir una reconstrucción exacta.
4. **Riesgo y capital:** extraerlos de A. No escoger nuevos stops, apalancamiento, posición o capital para beneficiar a C.
5. **Potencia y cobertura temporal:** no sustituir semanas/regímenes por millones de ticks correlacionados de una tarde.

## 2. Preguntas e hipótesis prerregistradas

- H1: C supera a B fuera de muestra; ¿hay utilidad adicional a un readout simple?
- H2: C supera a D y D2; ¿hay valor atribuible a estructura biológica, y no solo memoria/no linealidad/dimensión?
- H3: A filtrado por C mejora A bajo las mismas reglas de riesgo y supera filtros B, D y rechazos aleatorios equivalentes.
- H4 secundaria: C identifica oportunidades incrementales en las que A se abstiene.
- H5 secundaria: el efecto cambia en regímenes definidos causalmente de antemano.

El endpoint primario financiero será **diferencia de retorno neto de cartera por día sobre el mismo capital inicial**, con días sin operaciones incluidos. Endpoint primario predictivo: pérdida de predicción neta por oportunidad común (MSE para el readout ridge propuesto). Beneficio aislado, win rate aislado o coincidencia con un rival no satisfacen las hipótesis.

Antes de abrir validación/test: fijar en `protocol.json` el efecto mínimo útil `delta_min`, en puntos básicos de capital por día, y el margen tolerable de deterioro de drawdown. Elegirlos con costes, incertidumbre de ejecución y necesidad económica, **no según el resultado del modelo**. Registrar el valor y justificación. Objetivo de potencia: 80% para ese efecto; estimar duración con dependencia temporal sobre train. Un mínimo exploratorio de 200 trades cerrados OOS no sustituye ese cálculo ni garantiza independencia.

## 3. Brazos del experimento

| Brazo | Transformación | Qué se puede entrenar |
|---|---|---|
| A | Sistema actual exacto | Nada; misma configuración y lógica |
| B | Features de mercado, incluyendo los mismos lags → ridge multisalida | Readout lineal regularizado |
| C | Mismas features → encoder fijado → MaleCNS congelado → readout | Solo readout; normalización/PCA ajustadas dentro de train |
| D | Mismo encoder → reservoir aleatorio comparable → mismo readout | Igual que C |
| D2 | Reservoir disperso aleatorio con capacidad comparable | Igual que C |
| A+C | A emite entrada; C permite solo si coincide en dirección | Sin cambiar tamaño, stop, TP, salida ni riesgo de A |
| A+B, A+D | Controles del filtro | Mismas restricciones |
| A+rechazo aleatorio | Retener fracción comparable de propuestas de A | Ningún ajuste a resultados futuros |

**B debe tener memoria comparable en las entradas:** proporcionar el mismo historial causal de features/retardos, no solo la última vela contra un reservoir con memoria. Si se añade PCA o proyección de igual dimensión como ablation, registrarla como brazo adicional; no cambiar silenciosamente B.

A queda intacto. Se distinguen dos evaluaciones: (i) **calidad de señal**, con una política de ejecución/salida/riesgo común tomada de A; (ii) **reproducción end-to-end de A**, que conserva además su calendario de eventos, reentradas y estado. Si la separación del motor altera A, primero reparar el adaptador o declarar que A no se pudo reproducir: nunca llamar “A sin modificaciones” a una estrategia aproximada.

### Control de reservoir que realmente pueda refutar C

D debe preservar, hasta tolerancias declaradas: número de nodos y conexiones, distribución de pesos/signos, grados de entrada/salida, sparsity, dinámica LIF, dt, pasos por decisión, ruido, normalización, amplitud de entrada, número/identidad funcional de entradas y dimensión de readout. Usar rewiring dirigido que preserve grados y restricciones de signo por neurona cuando corresponda; verificar que altera motivos/conectividad y que no sea solo renombrar nodos.

Una permutación de etiquetas con entradas y salidas permutadas de forma equivalente deja la misma red; **no es un control nulo**. D2 destruye más estructura conservando tamaño, densidad, signos y escala, para comprobar sensibilidad al nulo elegido. Si algún atributo no puede preservarse simultáneamente, documentar la discrepancia y hacer una ablation específica; no afirmar “equivalente” sin diagnóstico.

Usar mismo encoder y canales de lectura en C/D; mismos estados iniciales, seeds de ruido y presupuestos de entrenamiento emparejados. No ajustar solo C hasta hacerlo dinámicamente activo y dejar D saturado. Diagnosticar actividad/saturación sin labels y con reglas compartidas. Si se usan neuronas descendentes seleccionadas por biología, mantener máscara fija en el control y añadir una máscara aleatoria comparable como sensibilidad, para separar efecto de wiring y selección de puertos.

Pilotaje con 5 grafos aleatorios y 3 seeds de dinámica, **sin conclusión confirmatoria**. Confirmación: 199 grafos por familia de nulo y 3 seeds compartidas, o justificar por adelantado un diseño estadístico alternativo con potencia suficiente. Comparar contra distribución y percentiles de D, no un seed especialmente malo ni solo la media. Si ese coste excede el presupuesto, declarar experimento limitado; no rebajar los controles después de ver quién gana.

El readout y su búsqueda usan exactamente el mismo algoritmo y grid en B/C/D. Propuesta económica: ridge con λ ∈ {0.01, 0.1, 1, 10}. C/D comparten dimensión de estados/readout. Encoder, dt, ganancia, ruido, proyección y pasos quedan congelados antes del test. Si se ajustan, cuentan como hiperparámetros y ensayos registrados; no son “gratis” por estar fuera del readout.

## 4. Dataset idéntico y disponible en cada instante

Crear un único dataset con hashes y versiones, consumido por todos los brazos. Universo: **todos los tokens Pons V2 elegibles por reglas comunes observables**, incluidos muertos, rugs, baja liquidez y retirados. La activación de distribuidor entra al universo solo cuando habría sido conocida. No elegir tokens por haber pagado, subido, sobrevivido o sido comprados por el rival.

Cada fila debe tener al menos:

```text
chain, token_CA, quote_CA, event_id, event_time, observed_at, available_at,
block_hash, block_number, transaction_index, log_index,
bar_start, bar_close, OHLCV, valid_bar, tradeable_status,
reserve_state_asof, distributor_known_asof, epoch_known_asof,
feature_version, data_source, coverage_flags
```

Usar CA como clave. Registrar decimales reales. Cada feature incluye su linaje y `max(input.available_at) <= decision_time`. Las estimaciones retrospectivas de `available_at` se etiquetan como tales y reciben idéntica demora en todos los brazos. La prueba de viabilidad final debe usar observaciones prospectivas reales.

Velas propuestas: **1 s, cerradas**, construidas del mismo stream de operaciones. Antes de fijar fechas, comprobar si existen datos suficientes para esa resolución. Si solo hay 1 min, no recrear artificialmente una carrera de entradas de 25 s ni retocar A para operar por minutos. En ese caso el estudio de A debe esperar datos adecuados.

El reloj común reproduce eventos/timers originales de A y las actualizaciones de mercado; todos acceden al mismo historial causal. Las velas son una representación adicional compartida, no permiso para retrasar las decisiones originales de A. En cada instante elegible se evalúa B/C/D aunque A no opere, para medir oportunidades exclusivas. A puede ignorar un evento que su lógica original ignoraría.

Features iniciales económicas: retornos y volatilidad trailing, rangos de velas, volumen/flujo firmado, desequilibrio compras-ventas, edad del token, reserva relativa, drawdown trailing, concentración conocida y metadatos/época disponibles. Igual información para todos. No introducir actividad futura del rival, máximos del día completo, volúmenes finales ni futuras asignaciones de dividendos. La identidad del rival es evaluación auxiliar, no label de rentabilidad.

No rellenar con precio futuro. Velas sin trades pueden transportar último precio con bandera explícita, pero eso **no crea liquidez ejecutable**. Una desaparición del token no borra su posición ni la liquida al último precio favorable.

## 5. Labels, separación temporal y estado neuronal

Para B/C/D, propuesta de target: vector del resultado neto de ejecutar LONG y, si es factible, SHORT con la **misma política congelada de A**, más opción cash=0. Entrenar ridge multisalida; aplicar umbral económico fijado en validación para LONG/SHORT/NO TRADE. El thresholding sigue igual procedimiento y grid en B/C/D. El modelo recibe únicamente features de decisión; los resultados futuros son labels disponibles **solo después de cerrar su horizonte**.

Si A no tiene horizonte máximo finito, fijar para el subestudio predictivo un horizonte de evaluación H común, explícito y separado de la reproducción de A; esto no cambia sus salidas reales en el backtest. No entrenar con un resultado de trade todavía abierto ni inventar el cierre. Documentar la diferencia entre target predictivo y resultado end-to-end.

Separación exterior propuesta: **60% train / 20% validation / 20% test final**, por fechas UTC comunes a todos los tokens. Registrar fechas reales tras inventariar cobertura y **antes de observar performance**. Todo dato ya examinado para diseñar reglas queda como desarrollo; no volver a etiquetarlo “OOS virgen”. Si el historial de este mercado es demasiado corto, reservar datos futuros.

Dentro del 80% de desarrollo: walk-forward expansivo con al menos 5 bloques de evaluación si la duración lo permite. Cada fold entrena solo hacia atrás. El test final se abre una sola vez cuando modelos, umbrales y análisis estén firmados/hashados. En walk-forward dentro de test, los reentrenamientos usan solo labels ya madurados, bajo calendario fijado antes de entrar; no modificar la regla a la vista de resultados parciales.

Purga de intervalos: eliminar de train observaciones cuyo label/horizonte de posición invada validación o test. Separar los cortes con un embargo predefinido por el mayor horizonte de labels y memoria relevante. Los lags causales anteriores al corte pueden servir de contexto; no se exige borrarlos artificialmente, pero nunca se usan labels del período evaluado. Si hay posiciones abiertas al corte, usar una política única prerregistrada de calentamiento/cartera y marcar carry-over; no cerrar solo las de un modelo para embellecerlo.

Normalización, imputación, selección de features, PCA, calibración y pesos de clase se ajustan únicamente en train de cada fold. Nada de k-fold aleatorio, leave-one-token-out con futuro en train, normalización global o PCA sobre todo el período.

Estados del reservoir: una secuencia independiente por token, orden temporal estricto y warm-up idéntico C/D. Un único cerebro reutilizado entre tokens sin reset introduciría dependencia del orden de iteración. Al cambiar fold: reset y warm-up desde pasado permitido; no reutilizar un estado que haya consumido test ni escoger el mejor reset después de medir. Seeds y estado inicial archivados. Para tokens nuevos, regla de warm-up/falta de historia igual para todos.

## 6. Motor común de ejecución y riesgo

Construir primero este motor y probar A contra fixtures y registros conocidos. No generar resultados de C antes de validar lo básico.

- Capital inicial, unidad contable, sizing, tope de posiciones, límites diarios, prioridad de órdenes simultáneas, stops/TP y gestión de reentradas: snapshot de A, iguales para todos. Sin presupuesto infinito en portafolios paralelos.
- Decisión después de cerrar la vela/recibir evento. Entrada a la primera cotización alcanzable **después de decisión + demora**; jamás al close que produjo la señal si no era ejecutable entonces.
- Primera comparación de señal: misma demora común conservadora y misma ejecución para A/B/C/D, para no confundir selección con hardware. Segunda evaluación de viabilidad: añadir latencia real medida de cada modelo; mostrar ambas. La mosca no puede tardar segundos y reclamar un fill de hace milisegundos.
- Mismo fee de plataforma, protocolo, impuestos, gas, ruta, spread, slippage, impacto y costes de conversión de activos. No ejecutar A por ruta cara y C por directa para atribuir el ahorro a biología.
- Slippage dependiente de tamaño/liquidez cuando haya datos; un haircut constante es sensibilidad, no ejecución real. Stress idéntico 1×/1.5×/2× costes e incrementos de demora, fijados antes del test.
- Órdenes fallidas, fills parciales, allowances, gas de fallos, activo de cotización disponible y limitaciones de capital incluidos. Si no se reconstruyen, señalar el límite y no concluir ventaja real.
- Si OHLC no permite ordenar stop y TP dentro de la vela: usar datos de mayor resolución o convención adversa común; nunca elegir la ruta favorable por modelo.
- Shorts: requieren préstamo/instrumento, financiación, disponibilidad, margen y liquidación. Si faltan, no hay trades short ejecutables; se informa N/A y clasificación direccional por separado.

**Dividendos:** un ledger contrafactual no obtiene por magia el payout real de otra wallet. Sin fórmula de asignación validada y recreación de peso/snapshot/umbral, no asignar dividendos ficticios a C/D. Separar PnL de precio/costes y dividendos. Usar análisis de sensibilidad común, explícito, para los no identificables; si la ventaja depende de dividendos no verificables, decisión NEED MORE DATA. Excluirlos a todos da una comparación de precio acotada, no una evaluación completa de nuestra estrategia de dividendos.

## 7. Métricas y convenciones

Publicar por fold, test final, seed, dirección y régimen, además de agregado temporal OOS sin duplicar días solapados.

| Métrica | Convención |
|---|---|
| Net P&L | Equity final menos inicial y flujos externos; costes completos. Realizado y mark-to-market separados |
| Return % | 100 × (equity final / inicial − 1), mismo capital y moneda |
| Max drawdown | Mayor caída desde máximo de equity con posiciones abiertas y costes |
| Sharpe | Exceso de retorno diario de cartera / desviación, días sin trade incluidos; rf y anualización explícitos. Ajustar inferencia por autocorrelación |
| Sortino | Exceso sobre MAR fijado / downside deviation; declarar MAR, convención y frecuencia |
| Profit factor | Suma beneficios netos positivos / valor absoluto de pérdidas netas; sin pérdidas → indefinido/infinito con tamaño de muestra, no “excelente” |
| Win rate | Trades netos positivos / cerrados; break-even separado |
| Average win / loss | Media de ganancias y de pérdidas netas, con unidades |
| Expectancy | Media neta por trade, y p(win)×avg(win) − p(loss)×abs(avg(loss)); incluir ceros |
| Trades | Propuestos, aceptados, enviados simulados, fills, fallidos, cerrados y abiertos separados |
| Long / short | Mismas métricas separadas; short no ejecutable → N/A |
| R-multiple | PnL neto / riesgo monetario inicial fijado por stop de A. Sin riesgo/stop definido → N/A; no usar tamaño de posición como R ni añadir stops |
| Estabilidad OOS | Diferencia IS→OOS, dispersión por folds/seeds, peor fold, fracción de períodos positivos y concentración en pocos trades |

Añadir: exposición, turnover, tiempo en mercado, capacidad, drawdown duration, calibración y error predictivo por clase, Brier/log-loss solo si hay probabilidades calibradas, PR-AUC para clases raras. No llamar probabilidad a la salida ridge sin calibrar. Para A determinista, no fabricar scores probabilísticos; usar acciones y métricas compatibles.

Si el período es demasiado corto, Sharpe/Sortino anualizados se etiquetan como inestables; reportar también resultados no anualizados. No considerar velas contiguas ni seeds distintos como nuevas realizaciones independientes del mercado.

Regímenes: bullish/bearish/sideways mediante tendencia trailing de un índice/benchmark disponible entonces; alta/baja volatilidad mediante volatilidad trailing con cortes ajustados en train. Congelar benchmark, ventanas y thresholds antes del test. Regímenes por token como sensibilidad. Nunca usar rendimiento futuro para decidir cuál era el régimen en la entrada. Submuestras escasas → inconclusas y corrección por multiplicidad.

## 8. Acuerdos, desacuerdos y filtros

Construir una tabla de decisiones por `(token_CA, decision_time)` con acciones de A y C. No emparejar “la compra más cercana” mirando hacia adelante. Matriz completa 3×3 LONG/SHORT/NO TRADE; distinguir desacuerdo de dirección de abstención.

Cuatro cohortes obligatorias:

1. Ambos proponen la misma dirección: evaluar propuesta común con ejecución compartida.
2. Direcciones opuestas: simular ambos resultados factibles, mismos costes/capital; short imposible no se inventa.
3. A propone y C rechaza/opone: contrafactual del trade de A que se habría evitado, incluyendo ganadores perdidos.
4. C propone y A rechaza: oportunidades adicionales, con la misma política de riesgo y exclusión de capital ya utilizado.

**Filtro principal:** ejecutar una propuesta de entrada de A solo si C coincide en ese instante. Todas las reglas de salida/riesgo siguen siendo las de A. NO TRADE o dirección opuesta rechaza la entrada; no invierte la operación. El filtro se aplica a entradas, no a stops ni salidas de protección.

Dos análisis complementarios:

- **Ablation de señal:** fijar las propuestas originales y sus asignaciones de riesgo; los trades rechazados dejan efectivo sin reciclarlo. Aísla calidad de rechazo.
- **Cartera filtrada completa:** reproducir la política original con capital liberado. Documentar decisiones adicionales por capacidad y estado; no atribuir todo el cambio a mejor clasificación.

Comparar A+C contra A+B, A+D y rechazo aleatorio con tasa de retención fijada en validación. Para la atribución estadística puede condicionarse aleatoriamente al número de trades retenidos por período/dirección, sin observar sus resultados; etiquetarlo como nulo diagnóstico, no estrategia deployable. Mostrar pérdidas evitadas, ganancias sacrificadas y exposición, porque rechazar casi todo reduce drawdown por sí solo.

Caso inverso: C filtrado por A y cartera de propuestas exclusivas de C. No permitir que C consulte la acción de A si estamos evaluando C independiente. Probar filtros por régimen cuenta como hipótesis adicional y necesita OOS posterior.

## 9. Evidencia estadística

1. Comparaciones **emparejadas** sobre los mismos días/opciones de mercado. Reportar diferencias e IC95%, no comparar dos Sharpes sin incertidumbre.
2. Bootstrap por bloques temporales sincronizados entre modelos y tokens, que respete operaciones solapadas y shocks comunes. Longitud de bloque elegida en train según dependencia/horizonte; sensibilidades fijadas. 10,000 remuestreos son baratos sobre retornos ya calculados. Agrupar adicionalmente por evento/lanzamiento en sensibilidad; no remuestrear ticks IID.
3. Familia primaria explícita: C−B, C−D, C−D2, A+C−A, A+C−A+B, A+C−A+D, A+C−rechazo aleatorio. Control FWER con **Holm** a 5%, junto con intervalos simultáneos cuando corresponda. Análisis de regímenes y oportunidades exclusivas, secundarios con multiplicidad propia y etiqueta exploratoria si no tienen potencia.
4. Para el control biológico, comparar C con la distribución de grafos nulos bajo el mismo procedimiento completo de train/validation/test. Valor p de rango `(1 + nulos >= C)/(1 + número_de_nulos)` y limitaciones del nulo; con pocos seeds no hay resolución para significancia múltiple. No promediar scores de entrenamiento y llamarlo prueba OOS.
5. Registrar **todos** los ensayos, encoders, hiperparámetros, seeds y resultados, incluso abandonados. Reportar Deflated Sharpe como diagnóstico adicional de selección/no-normalidad, no sustituto de OOS ni ajuste automático de dependencia. Referencia: [Bailey y López de Prado](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf).
6. Exigir tamaño del efecto práctico y consistencia, no solo p<0.05. Sensibilidad al mayor ganador y a los cinco mayores contribuyentes: retirar solo para diagnóstico, jamás limpiar la tabla principal. Informar si un único token/régimen explica casi todo.
7. Un resultado no significativo **no prueba ausencia de alpha**. Para conclusión de ausencia práctica usar equivalencia respecto a ±delta_min, IC y potencia adecuados; si son anchos → NEED MORE DATA. Un beneficio aparente que desaparece ante controles/multiplicidad favorece conclusión 5, no una afirmación universal sobre el cerebro.
8. Si surge una nueva hipótesis al mirar test, ese test pasa a desarrollo para esa hipótesis y se necesita otro período futuro. No seguir abriendo el mismo test hasta que algo salga verde.

## 10. Recursos y tareas para un modelo económico

**Fase 0 — Inventario, sin entrenar.** Congelar A/config efectiva sin secretos; crear manifiesto de datos y tabla de faltantes. Resolver short, dividendos, stop/R, fechas y universo. Entrega `preflight.md`. No descargar gigabytes ni ejecutar terceros antes de saber que la comparación es viable.

**Fase 1 — Motor y A.** Adaptador aislado + ejecución común + métricas. Fixtures: no look-ahead; compras/ventas con costes; short no disponible; reversiones; orden intrabar ambiguo; capital ocupado; marca a mercado de pérdidas; dividendos desconocidos. Reproducir decisiones de A y reconciliar diferencias documentadas. Entrega `baseline_reproduction.md`. Si no reproduce A, no avanzar a C.

**Fase 2 — Dataset/splits.** Congelar fechas y hashes; construir features una vez; purga/embargo; auditoría de disponibilidad por columna. Prueba fuerte: perturbar datos posteriores a t y comprobar que ninguna señal/feature anterior cambia. Mantener holdout final fuera de los archivos que usa la búsqueda. Entrega `data_audit.md` y `splits.json`.

**Fase 3 — B y prueba de plumbing C/D.** Primero B y la política A con datos train. Para C/D: inspeccionar dependencias y licencias, crear entorno aislado, fijar dataset neuronal/checksums; benchmark de 1,000 decisiones para memoria y tiempo. Tope propuesto de pilotaje: **4 horas de cómputo local**, sin nube pagada. No reducir la red solo para C y compararla con D de tamaño diferente. Un subgrafo es otro experimento y debe llamarse así.

**Fase 4 — Prerregistro completo.** Rellenar todos los `null` críticos en el JSON. Fijar encoder, warm-up, readout, seeds, coste, delta_min, calendario y criterios. Calcular tiempo/disco del estudio confirmatorio; si 199 controles son inviables, detener con presupuesto insuficiente y diseño alternativo por revisar, no fingir evidencia usando un solo control débil.

**Fase 5 — Walk-forward de desarrollo.** Cachear estados congelados C/D por hash de datos+encoder+connectoma+seed+reset; entrenar diferentes readouts sin volver a simular el cerebro. Normalización/PCA siguen dentro de train de cada fold. Guardar tablas de todos los ensayos. Ninguna llamada RPC por iteración: datos adquiridos una vez, análisis offline.

**Fase 6 — Test OOS sellado.** Elegir una configuración por brazo con reglas idénticas de validación, ejecutar test una vez, bootstrap/contrastes y tabla final. No seleccionar el mejor seed en test. Evaluar coste/latencia real como segunda tabla de viabilidad, sin sobrescribir la de señal.

**Fase 7 — Shadow prospectivo.** Solo si las etapas anteriores son válidas. Generar órdenes simuladas completas, fills/costes alcanzables y salidas bajo el mismo riesgo, no simples avisos. Duración determinada por potencia y cobertura, sin detener al obtener verde. Mantener el bot real intacto.

**Fase 8 — Informe de decisión.** Elegir conclusión con reglas de la sección siguiente. Si no hay datos suficientes, entregar las tablas con N/A y motivo, sin rellenar con números inventados.

Estructura propuesta (a construir; estos comandos/módulos aún no existen):

```text
baseline_snapshot/         # versión inmutable de A y configuración sin secretos
manifests/                 # datos, conectoma, costes, software, seeds, splits
adapters/                  # A, B, C, D con interfaz idéntica
features/                  # cálculo causal y linaje
execution/                 # fills, cartera, riesgo y costes comunes
experiments/               # protocolo y registro de todos los ensayos
results/<run_id>/          # señales, trades, equity, métricas, IC y reporte
```

Interfaz mínima propuesta: `observe(event_asof)`, `signal(token, decision_time) -> direction, score, model_version`, `reset(context_past_only)`. El simulador, no cada modelo, aplica ejecución/riesgo. Verificación automática de `available_at`, `fit_end`, hashes del split y ausencia de secretos. No implementar conexiones de envío.

## 11. Reglas de conclusión

No forzar una de las cinco conclusiones si el experimento no se ejecutó o no tiene potencia. En ese caso indicar insuficiencia y **NEED MORE DATA**.

- **CONCLUSION 1 — MaleCNS añade alpha.** C tiene mejora práctica OOS con IC y multiplicidad adecuados frente a B y ambos controles D; resultados consistentes entre períodos/seeds, riesgo no deteriorado más allá del margen y costes/latencia reales compatibles. Si además mejora el sistema existente o aporta una cartera incremental válida sin romper riesgo → **YES** para integración posterior controlada, nunca autorización automática para dinero real.
- **CONCLUSION 2 — MaleCNS no añade alpha.** Estudio válido y suficientemente potente demuestra equivalencia práctica/no mejora útil frente a controles y tampoco mejora A como filtro → **NO**. No usar simple falta de significancia como demostración de ausencia.
- **CONCLUSION 3 — MaleCNS no sirve solo, pero mejora nuestro sistema como filtro.** A+C supera A y filtros B/D/aleatorios en OOS, efecto práctico, robustez y costes; C independiente no pasa criterios → **ONLY AS FILTER**.
- **CONCLUSION 4 — MaleCNS funciona únicamente en determinados regímenes.** Interacción y ventaja en regímenes predefinidos replicadas OOS, detector de régimen causal y potencia suficiente. Si la política restringida no fue validada en datos nuevos → **NEED MORE DATA**. Si lo fue, **ONLY AS FILTER** para esa restricción; no generalizar al mercado completo.
- **CONCLUSION 5 — La mejora encontrada no supera adecuadamente los controles y probablemente es ruido/overfitting.** El resultado atractivo de desarrollo no sobrevive al test/controles/multiplicidad, o depende de elegir un seed/período. → **NO** a integrar esa versión; no afirmar que se ha probado imposible cualquier utilidad futura.

Para atribuir valor al **connectoma biológico**, superar B no basta: C debe superar controles D adecuados. Si C y D mejoran A por igual, puede existir utilidad de reservoirs, pero no una justificación específica para MaleCNS.

## 12. Tabla final exigida y anexos

Esta es una **plantilla pendiente**, no resultados. La tabla final reportará solo el test OOS común; desarrollo se publica aparte. Para D: seed prerregistrado para la trayectoria de ejemplo y distribución/IC de todos los seeds; no promediar capitales de cientos de carteras como si fueran una cartera única.

| Sistema | P&L neto | Max DD | Sharpe | PF | WR | Trades | Expectancy | OOS |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Sistema actual | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No ejecutado |
| Baseline ML | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No ejecutado |
| MaleCNS | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No ejecutado |
| Random reservoir | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No ejecutado |
| Sistema + MaleCNS filter | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No ejecutado |

Anexos obligatorios: Return %, Sortino, average win/loss, R, long/short, regímenes, folds/seeds, IC95% de diferencias, pruebas ajustadas, costes/latencia, matriz 3×3, trades rechazados rentables/perdedores, oportunidades exclusivas, filtros de control y limitaciones de dividendos/shorts. Incluir dataset/splits/commits/hashes y comando de reproducción cuando exista implementación.

**¿Deberíamos integrar el cerebro de mosca a nuestro sistema de trading actual?**

**NEED MORE DATA.** En este momento solo se preparó el protocolo y se inspeccionó código. No se han ejecutado backtests comparables, controles aleatorios ni evaluación financiera out-of-sample; el sistema de señales previo tampoco simula fills/PnL. No existe evidencia concreta para responder YES o ONLY AS FILTER todavía.
