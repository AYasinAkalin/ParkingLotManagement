# __main__.py
import database
import server
import config
import dependencies
import definitions
definitions.init()

# Install dependencies
reqs = dependencies.Dependency()
reqs.install_all()

# Set the database
db = database.Database(config.FILE_DATABASE)
db.create(clean=config.CLEAN_DB)
db.test(verbose=config.VERBOSE)
db.populate()

# Set the server and run it
server = server.Server(config.FILE_FLASK, config.DEBUG)
server.start()
