### Documentation for IANode Header Model Implementation

#### Overview

The IANode Header Model, as part of a data processing pipeline, facilitates the creation and management of security labels. 
The implementation involves creating a model that dynamically builds 
security labels, which can then be attached to data records. This process ensures that each record complies with specified 
security and access policies.

#### Classes 

1. **IANodeMixin Class**: An abstract base model providing core functionality
   - `build_security_labels(self)`: An abstract method that must be implemented by
      subclasses to utilize the SecurityLabelBuilder for constructing security 
      labels based on model attributes.
     
2. **IANodeModel Class (inherits IANodeMixin)**: Represents the IANode policy with various attributes.
   - Pro 


#### Example: Using IANode Header Model with Adapter

```python
import requests
from ianode_lib import Adapter
from ianode_lib.access import IANodeModel
from ianode_lib.records import Record, RecordUtils
from ianode_lib.sinks import KafkaSink

def records_from_file() -> list[str]:
    url = "https://test.com/wordlist.10000"
    resp = requests.get(url)
    resp.raise_for_status()
    lines = resp.text.rstrip().split("\n")
    return lines

# Create a sink and an adapter
sink = KafkaSink(topic="adapter-demo", broker="localhost:9092")
adapter = Adapter(target=sink, name="Demo Adapter with IANode Policy", source_name="Word List MIT")

data_header = {
    # IANode policy details...
}

# Validates data header against a model
data_header_obj =  IANodeModel(**data_header) 
# Builds labels from data header object
security_labels = data_header_obj.build_security_labels()

try:
    adapter.run()
    adapter.expect_records(10000)

    for i, line in enumerate(records_from_file(), start=1):
        record = Record(headers=None, key=i, value=line, raw=None)
        # The format representing a security policy header is defined at user discretion, code below is an example.
        record_with_headers = RecordUtils.add_headers(record, [('policyInformation', 
                                                                {'DH': data_header_obj.model_dump()})])
        record = RecordUtils.add_headers(record_with_headers, [('Security-Label', security_labels)])
        adapter.send(record)

    adapter.finished()
except KeyboardInterrupt:
    adapter.aborted()

if __name__ == '__main__':
    adapter.run()
```

#### Usage with Automatic Adapters

```python
   import json
   from pathlib import Path
   from typing import Iterable
   from ianode_lib import AutomaticAdapter, Record
   from ianode_lib.sinks import KafkaSink, Serializers
   
   data_header = {
       # IANode policy details...
   }
  
   # Validates data header against a model
   data_header_obj =  IANodeModel(**data_header) 
   # Builds labels from data header object
   security_labels = data_header_obj.build_security_labels()
   
   def read_json_objects(file_path):
       path = Path(file_path)
       with path.open('r', encoding='utf-8') as file:
           data = json.load(file)
           if not isinstance(data, list):
               raise ValueError("JSON file does not contain an array of objects")
           yield from data
   
   def generate_records() -> Iterable[Record]:
       for i, record in enumerate(read_json_objects("./demo_data.json")):
           record = Record(headers=None, key=i, value=record, raw=None)
           
           if condition:
               # The format representing a security policy header is defined at user discretion, code below is an example.
               record_with_headers = RecordUtils.add_headers(record, [('policyInformation', 
                                                                   {'DH': data_header_obj.model_dump()})])
               record = RecordUtils.add_headers(record_with_headers, [('Security-Label', security_labels)])
           yield record
   
   sink = KafkaSink(topic="output-automatic-adapter-demo", broker="localhost:9092", value_serializer=Serializers.to_json)
   adapter = AutomaticAdapter(target=sink, adapter_function=generate_records,
                              name="Example Automatic Adapter with security policy", source_name="Some file")
   
   if __name__ == '__main__':
       adapter.run()
```