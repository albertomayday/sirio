from openclaw import Agent

agent = Agent(name="OpenClaw_VERIFACTU")

agent.add_task("generar_registro", module="backend.generate_record")
agent.add_task("encadenar_hash", module="backend.hash_chain")
agent.add_task("firmar_registro", module="backend.sign_record")
agent.add_task("guardar_bd", module="backend.store_immutable")
agent.add_task("enviar_aeat", module="backend.send_aeat")
agent.add_task("validar_respuesta", module="backend.validate_aeat_response")

agent.save("workflow_verifactu.yaml")
