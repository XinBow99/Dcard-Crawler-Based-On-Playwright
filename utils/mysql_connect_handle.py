import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from utils import dcard_orm


class labDBconnect:
    def __init__(self, dbConfig=None):
        _database = 'dcard_crawler'
        remoteConfig = self.loadConfig(dbConfig)
        remoteConfig = remoteConfig[_database]
        self.host = remoteConfig['host']
        self.user = remoteConfig['user']
        self.password = remoteConfig['password']
        self.database = _database
        self.port = remoteConfig['port']
        self.charset = remoteConfig['charset']
        dbConnectString = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"
        self.dbConnectEngine = create_engine(dbConnectString)
        self.dbSession = sessionmaker(self.dbConnectEngine)

        print('Preparing to connect to database')

    def loadConfig(self, configFile):
        """
        Loads the config file and returns the config dictionary
        Args:
            configFile (_type_): yaml file with the database config
        """
        with open(configFile, 'r') as ymlfile:
            # Load the config file
            cfg = yaml.safe_load(ymlfile)
            ymlfile.close()
        print("Config file loaded")
        return cfg

    def getDcardPosts(self):
        print('[GetDcardPosts]start to run')
        with self.dbConnectEngine.connect() as connection:
            with self.dbSession(bind=connection) as session:
                _dcardPosts = session.query(dcard_orm.Posts.href).all()
                session.close()
        return _dcardPosts

    def writeMainContentToDatabase(self, cls, content: dict):
        # This function is customized to write the main content to database, main content is the raw content of the post.
        with self.dbConnectEngine.connect() as connection:
            # create a connection
            with self.dbSession(bind=connection) as session:
                # create a session
                exists = session.query(dcard_orm.Contents.href).filter_by(
                    href=cls.postId).first() is not None
                # check if the postId exists, maybe we need call 'postId' instead of 'href'
                # TODO: replace 'href' to 'postId'
            if not exists:
                print('[{}]{}'.format(
                    str(content['contentCreatedAt']),
                    str(content['content']).replace('\n', ''))
                )
                session.add(
                    dcard_orm.Contents(
                        href=cls.postId,
                        content=content['content'].replace('\n', ''),
                        content_create_at=content['contentCreatedAt'],
                        created_at=datetime.now()
                    )
                )
                session.commit()
                session.close()
            else:
                print('[info] {} content already exists.'.format(cls.postId))
                session.close()

    def writeCommentToDatabase(self, cls: object, comment: dict):
        """
        This function is used to write the comment to database
        Args:
            comment(dict): the comment to be written, the comment should have the following keys:
                postId(str): the postId of the comment
                author(str): the author of the comment
                content(str): the content of the comment
                like(int): the like of the comment
        """
        if cls.postCount == cls.parserOptions.limit_comment and cls.parserOptions.limit_comment != -1:
            cls.stopCrawler = True
        else:
            with self.dbConnectEngine.connect() as connection:
                with self.dbSession(bind=connection) as session:
                    exists = session.query(dcard_orm.Comments.comment_key).filter_by(
                        comment_key=comment['comment_key']).first() is not None
                    if not exists:
                        print('[write|{}]{}'.format(
                            cls.postCount,
                            comment['content']))
                        session.add(
                            dcard_orm.Comments(
                                href=comment['postId'],
                                author=comment['author'],
                                content=comment['content'],
                                like=comment['like'],
                                comment_key=comment['comment_key'],
                                comment_created_at=comment['comment_created_at'],
                                created_at=datetime.now()
                            )
                        )
                        session.commit()
                        session.close()
                        cls.postCount += 1
                    else:
                        print('[info|{}] {} comment already exists.'.format(
                            cls.postCount,
                            comment['comment_key']))
                        session.close()

    def writePostInformationToDatabase(self, cls: object, content: dict):
        """
        This function is used to write the content to database
        Args:
            content (dict): content to be written, should be a dictionary, and have the following keys:
                'title': title of the article
                'forum': forum of the article
                'href': href of the article
        """
        if cls.postCount == cls.parserOptions.limit_post and cls.parserOptions.limit_post != -1:
            cls.stopCrawler = True
        else:
            with self.dbConnectEngine.connect() as connection:
                with self.dbSession(bind=connection) as session:
                    exists = session.query(dcard_orm.Posts.href).filter_by(
                        href=content['href']).first() is not None
                    if not exists:
                        print('[write|{}]{}'.format(
                            cls.postCount,
                            str(content['title']).replace('\n', ''),
                        ))
                        session.add(
                            dcard_orm.Posts(
                                title=content['title'].replace('\n', ''),
                                forum=content['forum'].replace('\n', ''),
                                href=content['href'].replace('\n', ''),
                                created_at=datetime.now()
                            )
                        )
                        session.commit()
                        session.close()
                        cls.postCount += 1
                    else:
                        print('[info|{}]{} is already in database'.format(
                            cls.postCount,
                            content['title']))
                        session.close()


if __name__ == "__main__":
    db = labDBconnect("config/my_sql.yaml")
    # db.connect()
    # db.close()
