const { Agent } = require("../openclaw/src/agent");
const { generarRegistro, enviarAEAT } = require("../modules/aeat_client/verifactu_skill");

const agent = new Agent("OpenClaw_VERIFACTU");
agent.addTask("generar_registro",  "modules/aeat_client/verifactu_skill");
agent.addTask("encadenar_hash",    "modules/aeat_client/verifactu_skill");
agent.addTask("enviar_aeat",       "modules/aeat_client/verifactu_skill");
agent.save("workflows/workflow_verifactu.yaml");

// Test real
const r1 = generarRegistro("T-001");
console.log("\n[Ticket T-001]", r1);
const r2 = generarRegistro("T-002", r1.hash);
console.log("[Ticket T-002]", r2);
console.log("[Cadena íntegra]", r2.hash !== r1.hash ? "✅" : "❌");

const resp = enviarAEAT(r1);
console.log("[AEAT response]", resp);

agent.run("workflows/workflow_verifactu.yaml");
