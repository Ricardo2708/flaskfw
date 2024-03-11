document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('verificarBtn').addEventListener('click', function(e) {
        e.preventDefault()
        var ruta = '/admin';

        fetch(ruta)
            .then(function(response) {
                if (!response.ok) {
                    Swal.fire({
                        title: "Flask Admin",
                        text: "migrations have not been carried out",
                        icon: "warning"
                    });
                }
                else{
                    window.location.href = '/admin';
                }
                
            })
            .catch(function(error) {
                alert(error.message);
            });
    });
});