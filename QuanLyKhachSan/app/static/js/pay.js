function Infopay() {
    if (confirm("Bạn chắc chắn thanh toán?") == true) {
        fetch("/pay").then(res => {
            console.info(res)
            return res.json()
        }).then(data => {
            location.reload()
        }).catch(err => {
            console.error(err)
        })
    }
}