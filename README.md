# ExportFileParser

### Overall intention
* Receives files, either in the format: 
  * CSV, OFX or ...
* Verifies file type and content
* Parses file and returns JSON 
  * This format will be the same for all file types
  * So we can then process the file