console.log('Validador Totémico activo');

(function($) {
  $(function() {
    $('#formulario_registro').on('submit', function(e) {
      // 🔥 NO usamos preventDefault
      // 🔥 NO usamos this.submit()

      // Lectura de campos
      const username          = $('#username').val().trim();
      const nombre            = $('#nombre').val().trim();
      const apellido          = $('#apellido').val().trim();
      const email             = $('#email').val().trim();
      const pw1               = $('#password1').val();
      const pw2               = $('#password2').val();
      const direccion         = $('#direccion').val().trim();
      const numero_dpto_casa  = $('#numero_dpto_casa').val().trim();
      const comuna            = $('#comuna').val().trim();
      const region            = $('#region').val().trim();

      // Validación
      const errors = {};
      const reLetters   = /^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{3,30}$/;
      const reUsername  = /^[A-Za-z0-9_]{3,30}$/;
      const reEmail     = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const rePw        = /^(?=.*\d)(?=.*[A-Z]).{6,18}$/;

      // Validaciones individuales (igual que antes)
      if (!username) {
        errors.username = 'Por favor ingrese un nombre de usuario';
      } else if (!reUsername.test(username)) {
        errors.username = 'Debe tener entre 3 y 30 caracteres y puede incluir números o guiones bajos';
      }

      if (!nombre) {
        errors.nombre = 'Por favor ingrese su nombre';
      } else if (!reLetters.test(nombre)) {
        errors.nombre = 'El nombre debe tener entre 3 y 30 letras';
      }

      if (!apellido) {
        errors.apellido = 'Por favor ingrese su apellido';
      } else if (!reLetters.test(apellido)) {
        errors.apellido = 'El apellido debe tener entre 3 y 30 letras';
      }

      if (!email) {
        errors.email = 'Por favor ingrese su correo electrónico';
      } else if (!reEmail.test(email)) {
        errors.email = `El email "${email}" no es válido`;
      }

      if (!pw1) {
        errors.password1 = 'Por favor ingrese una contraseña';
      } else if (!rePw.test(pw1)) {
        errors.password1 = 'Debe tener 6–18 caracteres, una mayúscula y un número';
      }

      if (!pw2) {
        errors.password2 = 'Por favor confirme su contraseña';
      } else if (pw1 !== pw2) {
        errors.password2 = 'Las contraseñas no coinciden';
      }

      if (!direccion) {
        errors.direccion = 'Por favor ingrese su dirección';
      } else if (direccion.length < 3 || direccion.length > 40) {
        errors.direccion = 'Debe tener entre 3 y 40 caracteres';
      } else if (!/\d+/.test(direccion)) {
        errors.direccion = 'Debe incluir numeración obligatoria';
      }

      if (!numero_dpto_casa) {
        errors.numero_dpto_casa = 'Por favor ingrese el número de Dpto/Casa';
      } else if (numero_dpto_casa.length > 10) {
        errors.numero_dpto_casa = 'Máximo 10 caracteres permitidos';
      }

      if (!comuna) {
        errors.comuna = 'Por favor ingrese su comuna';
      } else if (!reLetters.test(comuna)) {
        errors.comuna = 'Debe tener entre 3 y 30 letras';
      }

      if (!region) {
        errors.region = 'Por favor ingrese su región';
      } else if (!reLetters.test(region)) {
        errors.region = 'Debe tener entre 3 y 30 letras';
      }

      // Limpia errores previos
      $('#username-error, #nombre-error, #apellido-error, #email-error, #password1-error, #password2-error, #direccion-error, #numero_dpto_casa-error, #comuna-error, #region-error')
        .text('');

      // Muestra errores inline
      Object.entries(errors).forEach(([field, msg]) => {
        $(`#${field}-error`).text(msg);
      });

      // Si hay errores, alerta global y bloquea envío
      if (Object.keys(errors).length) {
        alert(Object.values(errors).join('\n'));
        e.preventDefault(); // Solo bloquea si hay errores
        return;
      }

      // 🔥 Si no hay errores, dejamos que el formulario se envíe normalmente
    });
  });
})(jQuery);
