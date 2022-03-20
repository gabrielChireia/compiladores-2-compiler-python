# compiladores-ii-compiler-python
## AVAFiles
    - Contains compiler program syntax and compiler body

## GeneratedFiles
    - Contains code generated files

## Generators
    - LexicGenerator.py -> generates the lexical compiler
    - HypotheticalMachineGenerator.py -> generates the hypothetical machine compiler
    - HypotheticalMachineRunner.py -> runs the hypothetical machine

## Runnable
    - Main.py -> runs all generators

## FAQ
    - Para rodar o código, basta executar Main.py
    - Para trocar as instruções da LALG, exclua os arquivos que estão dentro da pasta 'GeneratedFiles' e faça as alterações no arquivo AVAFiles/correto.lalg-v2.txt
    - Lembrando que as instruções tem de estar no padrão definido no arquivo AVAFiles/lalg-v2.txt