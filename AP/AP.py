import datetime
import subprocess
import time

interface = "wlp1s0"
dispositivos_antiguos=[]

def obtener_dispositivos_conectados():
    try:
        resultado = subprocess.check_output(['arp', '-a']).decode('utf-8')
        dispositivos =[]
        lineas=resultado.splitlines()
        for linea in lineas:
            palabras=linea.split()
            for palabra in palabras:
                if len(palabra) == 17:
                    dispositivos.append(palabra)

        print(f"Dispositivos conectados: {dispositivos}")
        return dispositivos
    except Exception as e:
        print(f"Error al obtener la lista de dispositivos conectados: {e}")
        return []

def notificar_administrador(mac_dispositivo):
    print("S'ha connectado el dispositivo de interés con MAC: ",mac_dispositivo)

def cargar_horarios_desde_archivo(archivo):
    horarios={}
    try:
        with open(archivo, 'r') as file:
            for linea in file:
                partes = linea.strip().split(' ')
                mac = partes[0]
                horario = partes[1]
                horarios[mac] = horario
    except Exception as e:
        print(f"Error al cargar los horarios desde el archivo: {e}")

    return horarios

def obtener_ip(mac):
    ip=""
    try:
        resultado = subprocess.check_output(['arp', '-a']).decode('utf-8')
        lineas=resultado.splitlines()
        for linea in lineas:
            palabras=linea.split()
            for palabra in palabras:
                if palabra == mac:
                    ip_par=palabras[1]

        for letra in ip_par:
            if letra not in "()":
                ip+=letra
        return ip
    
        
    except Exception as e:
        print(f"Error al intentar obtener la IP: {e}")
    

def verificar_acceso(mac,horarios):
    hora_actual = datetime.datetime.now().time()

    if mac in horarios:
        rango_horario = horarios[mac]
        inicio,fin = rango_horario.split('-')
        inicio = datetime.datetime.strptime(inicio, "%H:%M").time()
        fin = datetime.datetime.strptime(fin, "%H:%M").time()

        if inicio <= hora_actual <= fin:
            return True
        
    return False

def echar_dispositivo(mac, ip, interface):
    try:
        
        subprocess.call(['sudo', 'arp', '-d', ip])
        
        subprocess.call(['sudo', 'hostapd_cli', '-i', interface, 'deauthenticate', mac])
        
        print("Dispositivo con MAC:" ,mac, "e IP:",{ip},"desconectado exitosamente")

    except Exception as e:
        print(f"Error al desconectar el dispositivo: {e}")

def monitorear_dispositivos_de_interes():

    
    global dispositivos_antiguos
    while True:
        horarios = cargar_horarios_desde_archivo("mac_list.txt")
        dispositivos_conectados = obtener_dispositivos_conectados()
        
        
        for mac_dispositivo in dispositivos_conectados:
            if mac_dispositivo not in dispositivos_antiguos:
                if mac_dispositivo in dispositivos_de_interes:
                    print("Se ha conectado el dispositivo de interes: ",mac_dispositivo)

            if mac_dispositivo not in horarios or not verificar_acceso(mac_dispositivo,horarios):
                ip = obtener_ip(mac_dispositivo)
                echar_dispositivo(mac_dispositivo,ip,interface)
                
        dispositivos_antiguos=dispositivos_conectados        
        # Espera antes de volver a verificar
        time.sleep(5)  # Espera 5 segundos

if __name__ == "__main__":
    
    # Lista de dispositivos de interés (direcciones MAC)
    dispositivos_de_interes = ['2a:73:b5:a0:d3:4a', '28:16:7f:6f:6d:fe']
    print("Dispositivos de interés: ",dispositivos_de_interes)
    
    # Inicia el monitoreo
    monitorear_dispositivos_de_interes()
