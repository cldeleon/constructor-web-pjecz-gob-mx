Title: Versión Pública de Sentencias
Slug: consultas-sentencias
Summary: .
URL: consultas/sentencias/
Save_As: consultas/sentencias/index.html
Date: 2020-05-11 16:00
Modified: 2020-05-20 12:32
JavaScripts: consultas-sentencias.js


**Instrucciones:** Primero elija la entidad/distrito, luego la autoridad/juzgado, después presione el botón Mostrar. Espere a que se cargue la lista. Para buscar use el campo filtrar; una fecha se escribe como año-mes-día, por ejemplo _2020-05-20_ es 20 de mayo 2020.

<div id="elegirListaDeSentencias" class="form-row mb-3">
<div class="col"><select id="distritoSelect"></select></div>
<div class="col"><select id="autoridadSelect"></select></div>
<div class="col"><button id="mostrarButton" type="button" class="btn btn-primary">Mostrar</button></div>
</div>

<table id="listaDeSentencias" class="table" style="width:100%">
<thead>
<th>Fecha</th>
<th>Sentencia</th>
<th>Expediente</th>
<th>P. Género</th>
<th>Archivo</th>
</thead>
</table>
