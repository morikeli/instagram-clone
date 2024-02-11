(function () {
    var toastElements = document.getElementsByClassName('toast')

    for (const toastElement of toastElements) {
        const toast = new bootstrap.Toast(toastElement, {delay: 5000})
        toast.show()
    }

})()
