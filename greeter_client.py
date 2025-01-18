# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import DB.db_funtions as dbfuntions

#import DB.orm as ORM

import DB.schema as schema


from datetime import datetime
import time


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from sqlalchemy import (
    create_engine

)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
        
        print("Greeter client received: " + response.message)
        
        response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)
        
       # evaluetecardholder = dbfuntions.findcardholder(20,1)
       # print(evaluetecardholder)
        #schema.init_db()

        #sd= schema.badgeAccess(1,1)
        #print(sd)
        

        # Assuming you have a SQLAlchemy session
        badge_id = 1
        reader_id = 1
        check_datetime = datetime(2025, 1, 18, 10, 0)  # January 17, 2025, 2:00 PM
     
     
        # Database connection parameters
        DB_HOST = "localhost"
        DB_NAME = "jana"
        DB_USER = "yourusername"
        DB_PASSWORD = "your_password"
        DB_PORT="5432"


        # Configurar la conexión a PostgreSQL
        DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

        engine = create_engine(DATABASE_URL)
        
        start_time = time.time()  # Registrar el tiempo de inicio

          # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        has_access = schema.validate_badge_access(session, badge_id, reader_id, check_datetime)
        if has_access:
           print("Badge has access.")
        else:
           print("Badge does not have access.")


        end_time = time.time()  # Registrar el tiempo de finalización
        elapsed_time = end_time - start_time  # Calcular el tiempo transcurrido
        print(f"Query executed in {elapsed_time:.4f} seconds")
        





if __name__ == "__main__":
    logging.basicConfig()
    run()
