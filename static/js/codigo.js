document.addEventListener('DOMContentLoaded', function () {
    const btnEditar = document.getElementById('btn-editar');
    const btnCancelar = document.getElementById('btn-cancelar');
    const divConfirmarCancelar = document.getElementById('botoes-confirmar-cancelar');
    const inputs = document.querySelectorAll('input:not(#cpf)');  // Não desabilitar o CPF nem o email

    btnEditar.addEventListener('click', () => {
        // Habilita os inputs (inclusive o email)
        inputs.forEach(input => input.disabled = false);

        // Troca os botões
        btnEditar.style.display = 'none';
        divConfirmarCancelar.style.display = 'flex';
    });

    btnCancelar.addEventListener('click', () => {
        // Desabilita novamente os inputs
        inputs.forEach(input => input.disabled = true);

        // Reseta os valores para os originais
        document.querySelectorAll('input').forEach(input => {
            input.value = input.defaultValue;
        });

        // Troca os botões de volta
        divConfirmarCancelar.style.display = 'none';
        btnEditar.style.display = 'inline-block';
    });

    // O botão Confirmar submete o formulário normalmente
});


// página carrinho

function atualizarCarrinho(index, acao) {
  fetch("/remover_item", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest"
    },
    body: JSON.stringify({ index: index, acao: acao })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById("carrinho").innerHTML = data.html;
  })
  .catch(error => console.error("Erro:", error));
}

