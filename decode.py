import base64
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-e', '--encrypted_string', required = True ,help = "Pass the encrypted string here")

args = vars(parser.parse_args())

decoded_string = base64.b64decode(args['encrypted_string']).decode('utf-8')

print("Decoded String:", decoded_string)
