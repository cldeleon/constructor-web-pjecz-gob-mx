// Consultas Sentencias
$(document).ready(function() {

    $("#sentenciasDiv").hide();
    $("#sentenciasTable").hide();

    $("#distritoSelect").append(
        '<option value="0">Pleno del Tribunal Superior de Justicia</select>',
        '<option value="1">Tribunal Constitucional Local</select>',
        '<option value="2">Tribunales Especializados</select>',
        '<option value="3">Salas TSJ</select>',
        '<option value="4">Tribunales Distritales</select>',
        '<option value="5">Distrito de Saltillo</select>',
        '<option value="6">Distrito de Monclova</select>',
        '<option value="7">Distrito de Sabinas</select>',
        '<option value="8">Distrito de Rio Grande</select>',
        '<option value="9">Distrito de Acuña</select>',
        '<option value="10">Distrito de Torreón</select>',
        '<option value="11">Distrito de San Pedro de las colonias</select>',
        '<option value="12">Distrito de Parras de la Fuente</select>'
    );

    var options = [
        '<option value="test1">00: test 1</option><option value="test2">00: test 2</option>',

        '<option value="test1">01: test 1</option><option value="test2">01: test 2</option>',

        '<option value="test1">02: test 1</option><option value="test2">02: test 2</option>',

        '<option value="test1">03: test 1</option><option value="test2">03: test 2</option>',

        '<option value="test1">04: test 1</option><option value="test2">04: test 2</option>',

        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Civil Saltillo</option>' +
        '<option value="test2">Juzgado Segundo de Primera Instancia en Materia Civil Saltillo</option>' +
        '<option value="test2">Juzgado Tercero de Primera Instancia en Materia Civil Saltillo</option>' +
        '<option value="test2">Juzgado Cuarto de Primera Instancia en Materia Civil Saltillo</option>' +
        '<option value="test2">Juzgado Primero de Primera Instancia en Materia Familiar Saltillo</option>' +
        '<option value="test2">Juzgado Segundo de Primera Instancia en Materia Familiar Saltillo</option>' +
        '<option value="test2">Juzgado Tercero de Primera Instancia en Materia Familiar Oral Saltillo</option>' +
        '<option value="test2">Juzgado Cuarto de Primera Instancia en Materia Familiar Oral Saltillo</option>' +
        '<option value="test2">Juzgado Primero de Primera Instancia en Materia Mercantil Saltillo</option>' +
        '<option value="test2">Juzgado Segundo de Primera Instancia en Materia Mercantil Saltillo</option>' +
        '<option value="test2">Juzgado Tercero de Primera Instancia en Materia Mercantil Saltillo</option>' +
        '<option value="test2">Juzgado Primero de Primera Instancia en Materia Penal Saltillo</option>' +
        '<option value="test2">Juzgado Primero Letrado Civil Saltillo</option>' +
        '<option value="test2">Juzgado Segundo Letrado Civil Saltillo</option>' +
        '<option value="test2">Juzgado Segundo Penal Saltillo Especializado en Narcomenudeo</option>' +
        '<option value="test2">Juzgado de Primera Instancia en Materia Penal del Sistema Acusatorio y Oral Saltillo</option>' +
        '<option value="test2">Juzgado de Primera Instancia en Materia Familiar Auxiliar del Juzgado Segundo Familiar Saltillo</option>',

        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Civil Monclova</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Civil Monclova</option>' +
        '<option value="test1">Juzgado Tercero de Primera Instancia en Materia Civil Monclova</option>' +
        '<option value="test1">Juzgado Cuarto de Primera Instancia en Materia Familiar Monclova</option>' +
        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Familiar Monclova</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Familiar Monclova</option>' +
        '<option value="test1">Juzgado Tercero de Primera Instancia en Materia Familiar Monclova</option>' +
        '<option value="test2">Juzgado Primero de Primera Instancia en Materia Penal Monclova</option>',
        '<option value="test1">Juzgado de Primera Instancia Penal del Sistema Acusatorio y Oral Frontera</option>' +

        '<option value="test1">Juzgado de Primera Instancia en Materia Civil y Familiar Sabinas</option>' +
        '<option value="test1">Juzgado de Primera Instancia en Materia Familiar Sabinas</option>' +
        '<option value="test1">Juzgado de Primera Instancia en Materia Penal de Sabinas</option>' +
        '<option value="test1">Juzgado de Primera Instancia Penal del Sistema Acusatorio y Oral Sabinas</option>',
        '<option value="test1">Juzgado Sexto Auxiliar de Primera Instancia en Materia Familiar Sabinas</option>' +

        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Civil Piedras Negras</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Civil Piedras Negras</option>' +
        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Familiar Piedras Negras</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Familiar Oral Piedras Negras</option>' +
        '<option value="test1">Juzgado Primero Penal Piedras Negras Especializado en Narcomenudeo</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Penal Piedras Negras</option>' +
        '<option value="test1">Juzgado Tercero de Primera Instancia en Materia Penal Piedras Negras</option>' +
        '<option value="test1">Juzgado de Primera Instancia en Materia Penal del Sistema Acusatorio y Oral Piedras Negras</option>',

        '<option value="test1">Juzgado de Primera Instancia en Materia Civil Acuña</option>' +
        '<option value="test1">Juzgado de Primera Instancia en Materia Penal Acuña</option>' +
        '<option value="test1">Juzgado de Primera Instancia en Materia Familiar Acuña</option>' +
        '<option value="test2">Juzgado de Primera Instancia en Materia Penal del Sistema Acusatorio Y Oral de Acuña</option>',

        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Civil Torreón</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Civil Torreón</option>' +
        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Mercantil Torreón</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Mercantil Torreón</option>' +
        '<option value="test1">Juzgado Cuarto de Primera Instancia en Materia Civil Torreón</option>' +
        '<option value="test1">Juzgado Tercero de Primera Instancia en Materia Civil Torreón</option>' +
        '<option value="test1">Juzgado Tercero de Primera Instancia en Materia Mercantil Torreón</option>' +
        '<option value="test1">Juzgado Segundo Letrado Civil Torreón</option>' +
        '<option value="test1">Juzgado Quinto de Primera Instancia en Materia Familiar Oral Torreón</option>' +
        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Familiar Torreón</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Familiar Torreón</option>' +
        '<option value="test1">Juzgado Tercero de Primera Instancia en Materia Familiar Torreón</option>' +
        '<option value="test1">Juzgado Cuarto de Primera Instancia en Materia Familiar Torreón</option>' +
        '<option value="test1">Juzgado de Primera Instancia en Materia Penal del Sistema Acusatorio y Oral Torreon</option>' +
        '<option value="test1">Juzgado Primero de Primera Instancia en Materia Penal Torreón</option>' +
        '<option value="test1">Juzgado Segundo de Primera Instancia en Materia Penal Torreón</option>' +
        '<option value="test1">Juzgado Tercero de Primera Instancia en Materia Penal Especializado en Narcomenudeo Torreón</option>' +
        '<option value="test1">Juzgado Cuarto de Primera Instancia en Materia Penal Torreón</option>' +
        '<option value="test1">Juzgado Quinto de Primera Instancia en Materia Penal Torreón</option>',

        '<option value="test1">Juzgado de Primera Instancia en Materia Civil San Pedro</option>' +
        '<option value="test2">Juzgado de Primera Instancia en Materia Familiar Oral San Pedro</option>',

        '<option value="test1">Juzgado de Primera Instancia en Materia Civil y Familiar Parras</option>' +
        '<option value="test2">Juzgado de Primera Instancia en Materia Familiar Oral de Parras</option>'
    ];

    $("#distritoSelect").change(function() {
        var val = $(this).val();
        $("#autoridadSelect").html(options[val]);
    });

    $("#mostrarButton").click(function(){
        console.log("Botón presionado")
    });

    $("#sentenciasDiv").show();

} );
