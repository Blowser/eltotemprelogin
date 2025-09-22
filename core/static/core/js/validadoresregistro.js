// core/static/core/js/validadoresregistro.js
console.log('Validador Totémico activo');

(function($) {
  $(function() {
    $('#formulario_registro').on('submit', function(e) {
      e.preventDefault();

      // Lectura de campos
      const username  = $('#username').val().trim();
      const nombre    = $('#nombre').val().trim();
      const apellido  = $('#apellido').val().trim();
      const email     = $('#email').val().trim();
      const pw1       = $('#password1').val();
      const pw2       = $('#password2').val();
      const direccion = $('#direccion').val().trim();
      const comuna    = $('#comuna').val().trim();
      const region    = $('#region').val().trim();

      // Validación
      const errors = {};
      const reLetters = /^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{3,30}$/; // incluye espacios y tildes
      const reEmail   = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const rePw      = /^(?=.*\d)(?=.*[A-Z]).{6,18}$/;

      // Nombre de usuario
      if (!username) {
        errors.username = 'Por favor ingrese un nombre de usuario';
      } else if (!reLetters.test(username)) {
        errors.username = 'El nombre de usuario debe tener entre 3 y 30 letras';
      }

      // Nombre
      if (!nombre) {
        errors.nombre = 'Por favor ingrese su nombre';
      } else if (!reLetters.test(nombre)) {
        errors.nombre = 'El nombre debe tener entre 3 y 30 letras';
      }

      // Apellido
      if (!apellido) {
        errors.apellido = 'Por favor ingrese su apellido';
      } else if (!reLetters.test(apellido)) {
        errors.apellido = 'El apellido debe tener entre 3 y 30 letras';
      }

      // Email
      if (!email) {
        errors.email = 'Por favor ingrese su correo electrónico';
      } else if (!reEmail.test(email)) {
        errors.email = `El email "${email}" no es válido`;
      }

      // Contraseña
      if (!pw1) {
        errors.password1 = 'Por favor ingrese una contraseña';
      } else if (!rePw.test(pw1)) {
        errors.password1 = 'La contraseña debe tener 6–18 caracteres, una mayúscula y un número';
      }

      // Confirmar contraseña
      if (!pw2) {
        errors.password2 = 'Por favor confirme su contraseña';
      } else if (pw1 !== pw2) {
        errors.password2 = 'Las contraseñas no coinciden';
      }

      // Dirección: 3–40 caracteres + dígito
      if (!direccion) {
        errors.direccion = 'Por favor ingrese su dirección';
      } else if (direccion.length < 3 || direccion.length > 40) {
        errors.direccion = 'La dirección debe tener entre 3 y 40 caracteres';
      } else if (!/\d+/.test(direccion)) {
        errors.direccion = 'La dirección debe incluir numeración obligatoria';
      }

      // Comuna 3–30 caracteres
      if (!comuna) {
        errors.comuna = 'Por favor ingrese su comuna';
      } else if (!reLetters.test(comuna)) {
        errors.comuna = 'La comuna debe tener entre 3 y 30 letras';
      }

      // Región 3–30 caracteres
      if (!region) {
        errors.region = 'Por favor ingrese su región';
      } else if (!reLetters.test(region)) {
        errors.region = 'La región debe tener entre 3 y 30 letras';
      }

      // Limpia errores previos
      $('#username-error, #nombre-error, #apellido-error, #email-error, #password1-error, #password2-error, #direccion-error, #comuna-error, #region-error')
        .text('');

      // Muestra errores inline
      Object.entries(errors).forEach(([field, msg]) => {
        $(`#${field}-error`).text(msg);
      });

      // Si hay errores, alerta global
      if (Object.keys(errors).length) {
        alert(Object.values(errors).join('\n'));
        return;
      }

      // Éxito: envía el formulario
      this.submit();
    });
  });
})(jQuery);
