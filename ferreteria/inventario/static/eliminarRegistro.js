(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminar");

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const del = confirm('¿Seguro de eliminar?');
            if (!del) {
                e.preventDefault();
            }
        });
    });
    
})();