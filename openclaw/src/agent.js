const yaml = require("js-yaml");
const fs = require("fs");
const path = require("path");

class Agent {
  constructor(name) {
    this.name = name;
    this.tasks = [];
    console.log(`[OpenClaw] Agente '${name}' inicializado`);
  }
  addTask(taskName, module) {
    this.tasks.push({ task: taskName, module });
    console.log(`[OpenClaw] Tarea: ${taskName} -> ${module}`);
  }
  save(filePath) {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, yaml.dump({ agent: this.name, tasks: this.tasks }));
    console.log(`[OpenClaw] Workflow guardado: ${filePath}`);
  }
  run(workflowPath) {
    const wf = yaml.load(fs.readFileSync(workflowPath, "utf8"));
    console.log(`[OpenClaw] Ejecutando: ${workflowPath}`);
    wf.tasks.forEach(t => {
      try {
        require(`../../${t.module}`);
        console.log(`  ✅ ${t.task}`);
      } catch(e) {
        console.warn(`  ⚠️  ${t.task}: ${e.message}`);
      }
    });
  }
}

module.exports = { Agent };
