const crypto = require("crypto");

function generarRegistro(ticket, hashAnterior = "0".repeat(64)) {
  const xml = `<Registro><Ticket>${ticket}</Ticket><HashAnterior>${hashAnterior}</HashAnterior></Registro>`;
  const hash = crypto.createHash("sha256").update(xml + hashAnterior).digest("hex");
  const qr = `https://verifactu.gob.es/verify?hash=${hash}`;
  return { xml, hash, qr };
}

function enviarAEAT(registro) {
  console.log(`[AEAT] Enviando registro hash=${registro.hash.slice(0,16)}... [simulado]`);
  return { csv: "CSV_SIMULADO_" + Date.now(), estado: "enviado" };
}

module.exports = { generarRegistro, enviarAEAT };
