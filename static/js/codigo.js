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




//Cria a area de pagamento
    function mostrarDiv() {
        document.getElementById("tela-inteira").classList.add("mostrar");
    }

    function fecharDiv() {
        document.getElementById("tela-inteira").classList.remove("mostrar");
    }



    // Scritps que gera o qrcode
    const valor = 123.456; // valor pré-definido
    const valorFormatado = valor.toFixed(2); // formata com 2 casas decimais

    const gerarBtn = document.getElementById('gerarBtn');
    const pagarBtn = document.getElementById('pagarBtn');
    const qrcodeDiv = document.getElementById('qrcode');
    const mensagemDiv = document.getElementById('mensagem');

    let qr;

    gerarBtn.addEventListener('click', () => {
      // Limpa QRCode anterior, se existir
      qrcodeDiv.innerHTML = "";
      mensagemDiv.textContent = "";

      // Gera QR Code com o valor formatado
      qr = new QRCode(qrcodeDiv, {
        text: valorFormatado,
        width: 200,
        height: 200,
      });

      // Mostra botão de pagamento
      pagarBtn.style.display = 'inline-block';
    });

    pagarBtn.addEventListener('click', () => {
      // Simula confirmação de pagamento
      mensagemDiv.textContent = "Pagamento realizado com sucesso!";
      pagarBtn.style.display = 'none';
      qrcodeDiv.innerHTML = ""; // limpa o QR Code
    });