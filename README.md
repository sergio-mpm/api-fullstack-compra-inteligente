# api-fullstack-compra-inteligente
API criada para o MVP da Disciplina: Sprint: Qualidade de Software, Segurança e Sistemas Inteligentes (40530010063_20260_01) - Pós-graduação de Engenharia de Software da PUC-Rio. Visando criar um sistema inteligente baseado em um modelo preditivo de compras. -> Criada por Sergio Gustavo M. P. Moreira

## Como Executar

Serão necessárias algumas instalações de dependências em sua máquina para utilizar o sistema. Caso queira recriar o modelo, basta seguir as instruções que seguem no notebook .ipynb contido neste repositório. O mesmo também se encontra no link: https://colab.research.google.com/drive/1qEE0vtk4YdcfAfvlIQ9aGuNAkEIF6CQC#scrollTo=qEbJHZOfzsc6

## Criando o ambiente virtual

Na pasta do projeto foi executado o comando para criação do ambiente virtual Python, utilizada a versão Python 3.12 para sua criação

O comando a ser utilizado para criação do ambiente virtual é 

--> python -m venv smartbuy_venv

Após isso será criado o ambiente virtual para o projeto e ali devem ser instaladas as dependencias do projeto.

Ative o ambiente virtual com o seguinte comando:

--> .smartbuy_venv/Scripts/activate.ps1

Assim aparecerá o ambiente virtual ativo antes do path e poderá instalar as dependencias com o seguinte comando:

--> python -m pip install requirements.txt

Como foi visto em projetos anteriores, alguns testes realizados em máquinas diferentes não instalaram totalmente suas dependencias, é recomendado que seja validada a instalação das bibliotecas que deram algum problema, seguem os comandos:

--> python -m pip install flask-cors
--> python -m pip install flask-openapi3
--> python -m pip install SQLAlchemy
--> python -m pip install -U flask-openapi3[swagger,redoc,rapidoc,rapipdf,scalar,elements]

Algumas dessas bibliotecas infelizmente não vieram junto ao executar a instalação dos requirements, sempre importante validar.

## Criando o banco de dados

O banco de dados da aplicação é gerado automaticamente através do flask migrate, um comando que utiliza as entidades (models) do nosso sistema para gerar as tabelas no banco de dados, principalmente com auxílio da biblioteca SQLAlchemy. Lembra bastante o famoso Entity-Framework.

Devemos iniciar a construção do banco de dados através do comando a seguir:

--> flask db init

Isso fará com que o sistema gere o database.db , que receberá os dados da nossa aplicação.

Após iniciar devemos gerar a primeira migration, que é um versionamento de instância do nosso banco de dados. Seguindo o comando:

--> flask db migrate -m "Estrutura Inicial da base de dados"

Assim criaremos uma migration com uma label de Estrutura Inicial da base de dados, nos ajudará a identificar esse primeiro passo.

Após isso feito, o comando para instanciar na base de dados deverá ser executado:

--> flask db upgrade

Assim, teremos todas nossas classes no banco de dados conforme previsto. Para esse sistemas estaremos utilizando o banco de dados para persistir os usuários que acessarão o sistema.
O intuito da criação da base de dados e desse conjunto de usuário é explorar aspectos do desenvolvimento de Software Seguro, através de uma criptografia de senha utilizando a biblioteca werkzeug.security, juntamente com a criação de um token de sessão (JWT) e um JWT_SECRET_KEY.
Em uma aplicação de mundo real, o ideal seria criar um arquivo de variáveis de ambiente .env para que o token JWT fosse instanciado nele, porém para fins didáticos o JWT_SECRET_KEY está sendo instanciado no arquivo config.py

## Uso de Desenvolvimento Seguro no sistema

Como mencionado anteriormente, o banco de dados foi construído para que pudéssemos explorar técnicas de desenvolvimento seguro como a criptografia de senha que se dá através de um comando importado da biblioteca werkzeug.security chamado generate_password_hash que faz a criptografia da senha e o usuário ao acessar o sistema, utiliza o serviço de autenticação com o método check_password_hash que realiza a leitura da senha criptografada para poder liberar o acesso ao sistema.

O uso do token JWT que é fornecido ao usuário quando ele acessa o sistema permite com que o acesso ao sistema seja garantido somente a usuários que tiveram a sessão iniciada e fornecidos com um token de acesso, sendo que esse token também expira com o tempo. Garante-se assim que o sistema tenha uma camada de proteção para quaisquer acessos indevidos, sendo somente permitida a execução dos métodos no sistema aquele que tiver sido autenticado e possuir o token JWT.

## Executando a aplicação

Agora que temos nosso ambiente configurado, nosso banco de dados instanciado, devemos iniciar a aplicação backend. O comando a seguir irá iniciar a aplicação:

--> python app.py

Assim, teremos nossa aplicação funcionando em ambiente local, normalmente configurada para a rota http://localhost:5000.

# Acessando o Swagger

Para acessar o Swagger, basta acessar a rota http://localhost:5000/v1/swagger

Assim conseguiremos testar os endpoints da aplicação com mockups e verificar todas as rotas que a API possui.