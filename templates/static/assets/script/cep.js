document.addEventListener("DOMContentLoaded", function () {
  const INPUT_CEP = document.getElementById("cep");
  const INPUT_LOGRADOURO = document.getElementById("endereco");
  const INPUT_NUMERO = document.getElementById("numero");
  const INPUT_BAIRRO = document.getElementById("bairro");
  const INPUT_CIDADE = document.getElementById("cidade");
  const INPUT_UF = document.getElementById("uf");
  const FEEDBACK_CONTAINER = document.getElementById("feedback-container");
  const FEEDBACK = document.getElementById("feedback");
  const FORM = document.getElementById("endereco-form");

  function validarCEP(cep) {
    if (!/^\d{8}$/.test(cep)) {
      throw new Error("CEP inválido. Insira um CEP válido (8 dígitos).");
    }
  }

  function exibirMensagemCarregamento() {
    FEEDBACK.innerText = "Buscando Informações do Endereço ...";
  }

  function limparCampos() {
    INPUT_LOGRADOURO.value = "";
    INPUT_CIDADE.value = "";
    INPUT_UF.value = "";
  }

  function preencherCamposComDados(json) {
    INPUT_LOGRADOURO.value = json.logradouro;
    INPUT_CIDADE.value = json.localidade;
    INPUT_BAIRRO.value = json.bairro;
    INPUT_UF.value = json.uf;
    INPUT_NUMERO.focus();
  }

  function exibirErroMensagem(error) {
    console.error(error);
    FEEDBACK.innerText = "CEP não encontrado ou ocorreu um erro na busca.";
  }

  FORM.addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o comportamento padrão de envio do formulário
  });

  INPUT_CEP.addEventListener("keydown", async (event) => {
    try {
      // Se a tecla pressionada foi Enter
      if (event.key === "Enter") {
        let cep = INPUT_CEP.value.trim(); // Certificando-se de que espaços em branco sejam removidos
        validarCEP(cep);
        exibirMensagemCarregamento();

        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);

        if (!response.ok) {
          throw new Error("CEP não encontrado");
        }

        const json = await response.json();

        limparCampos();
        preencherCamposComDados(json);

        FEEDBACK.innerText = ""; // Limpa a mensagem de feedback

        
      }
    } catch (error) {
      exibirErroMensagem(error.message);
    }
  });
});
