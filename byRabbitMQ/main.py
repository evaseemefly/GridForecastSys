import pika

def on_open(connection):
    # Invoked when the connection is open
    pass

# Create our connection object, passing in the on_open method
connection = pika.SelectConnection(on_open_callback=on_open)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()