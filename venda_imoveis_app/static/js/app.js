$(document).ready(() => {
    // toggle dropdown de opções dos clientes / imoveis
    $(".dropdown").click(function () {
        $(this).find(".dropdown-content").toggleClass("show");
    });

    // Recebe os dados do botão de edição e preenche o modal de edição de imoveis
    const modalBase = $('#modalCadastro')
    modalBase.on('show.bs.modal', function (e) {
        const button = e.relatedTarget
        let title = button.getAttribute('data-bs-title')
        let check = button.getAttribute('data-bs-check')
        let id = button.getAttribute('data-bs-id-imovel')
        let tipo = button.getAttribute('data-bs-tipo')
        let localizacao = button.getAttribute('data-bs-localizacao')
        let valor = button.getAttribute('data-bs-valor')
        let comissao = button.getAttribute('data-bs-comissao')

        $('#modalTitle').html(title)
        $('#check_edit').val(check)
        $('#id_imovel').val(id)
        $('#id_tipo').val(tipo)
        $('#id_localizacao').val(localizacao)
        $('#id_valor_0').val(parseFloat(valor))
        $('#id_comissao_vendedor_0').val(parseFloat(comissao))
    })

    // Recebe os dados do botão de edição e preenche o modal de edição de clientes
    modalBase.on('show.bs.modal', function (e) {
        const button = e.relatedTarget
        let title = button.getAttribute('data-bs-title')
        let check = button.getAttribute('data-bs-check')
        let id = button.getAttribute('data-bs-id-cliente')
        let nome = button.getAttribute('data-bs-nome')
        let cpf = button.getAttribute('data-bs-cpf')
        let email = button.getAttribute('data-bs-email')
        let telefone = button.getAttribute('data-bs-telefone')


        $('#modalTitle').html(title)
        $('#check_edit').val(check)
        $('#id-cliente').val(id)
        $('#id_nome').val(nome)
        $('#id_cpf').val(cpf)
        $('#id_email').val(email)
        $('#id_telefone').val(telefone)
    })

    // Altera o valor da comissão de acordo com a mudança do valor do imóvel
    $('#id_valor_0').val(0);
    $('#id_valor_0').on('change keyup', function () {
        $('#id_comissao_vendedor_0').val(getComissao());
    })
})

// Remove a visibilidade do botão de dropdown ao clicar fora do mesmo
window.onclick = function (e) {
    if (!e.target.matches('.btn-option') &&
        !e.target.matches('.dropdown') &&
        !e.target.matches('#icon-option')) {
        if ($(".dropdown-content").hasClass("show")) {
            $(".dropdown-content").removeClass("show");
        }
    }
}

// Calcula o valor da comissão de acordo com o valor do imóvel
const getComissao = () => {
    let valor = $('#id_valor_0').val();
    return parseFloat(valor * 0.05).toFixed(2);
}