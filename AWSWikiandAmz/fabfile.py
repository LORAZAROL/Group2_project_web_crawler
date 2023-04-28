from __future__ import with_statement
from fabric import Connection, Config, task, ThreadingGroup

hosts = ['52.207.96.247',
         '3.95.28.216']

connections = [Connection(
    host=host,
    user="ec2-user",
    connect_kwargs={
        "key_filename": "/Users/zhizhenzhou/Desktop/test01.pem",
    }
) for host in hosts]

@task
def install_packages_libraries(c):
    c.sudo('yum update')
    c.sudo('yum install python3.6 python3.6-pip')
    c.run('curl -O https://bootstrap.pypa.io/get-pip.py')
    c.run('python3 get-pip.py --user')
    c.run('pip3 install fake_useragent')
    c.run('pip3 install numpy')
    c.run('pip3 install beautifulsoup4')
    c.run('pip3 install pandas')
    c.run('pip3 install requests')
    c.run('pip3 install lxml')
    c.run('pip3 install cassandra-driver')
    c.sudo('yum install git')
    c.run('git clone https://https://github.com/ZhizhenZhou/Crawler')

@task
def install_redis_cli(c):
    # ssh connect install epel repo
    c.run('pip3 install redis')
    c.run('pip3 install redis-py-cluster')
    c.run('pip3 install redlock-py')


@task
def git_pull(c):
    with c.cd('/home/ec2-user/Crawler'):
        c.run('git stash')
        c.run('git pull origin master')

@task
def run_crawler(c):
    with c.cd('/home/ec2-user/Crawler/'):
        c.run('python3 wiki_crawler.py')

@task
def run_amzn_crawler(c):
    with c.cd('/home/ec2-user/Crawler/'):
        c.run('python3 amazon_search_description_crawler.py')

if __name__ == "__main__":
    connection = connections[0]
    connection.run('sudo yum install python36')
    install_packages_libraries(connection)
    install_redis_cli(connection)
    git_pull(connection)
    run_crawler(connection)