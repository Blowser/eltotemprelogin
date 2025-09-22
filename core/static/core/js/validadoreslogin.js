console.log('Validador Totémico de Login activo');

(function($) {
  $(function() {
    $('form').on('submit', function(e) {
      e.preventDefault();

      // Lectura de campos
      const username = $('#username').val().trim();
      const password = $('#password').val();

      // Validación
      const errors = {};
      const reUsername = /^[A-Za-z0-9_]{3,30}$/; // Letras, números y _ entre 3 y 30

      // Nombre de usuario
      if (!username) {
        errors.username = 'Por favor ingrese su nombre de usuario';
      } else if (!reUsername.test(username)) {
        errors.username = 'El nombre de usuario debe tener entre 3 y 30 caracteres y puede incluir números y _';
      }

      // Contraseña
      if (!password) {
        errors.password = 'Por favor ingrese su contraseña';
      } else if (password.length < 6 || password.length > 18) {
        errors.password = 'La contraseña debe tener entre 6 y 18 caracteres';
      }

      // Limpiar errores previos
      $('#username-error, #password-error').remove();
      
      // Mostrar errores inline
      Object.entries(errors).forEach(([field, msg]) => {
        const input = $(`#${field}`);
        input.after(`<small id="${field}-error" class="text-danger">${msg}</small>`);
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
