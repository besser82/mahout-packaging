Name:          mahout
Version:       0.7
Release:       1%{?dist}
Summary:       Scalable machine learning libraries
License:       ASL 2.0
Url:           http://mahout.apache.org/
Source0:       http://www.apache.org/dist/mahout/%{version}/%{name}-distribution-%{version}-src.tar.gz
#Source1:       ...
#Patch0:        ...
BuildRequires: java-devel
# 0.8
# http://gil.fedorapeople.org/randomizedtesting.spec
# http://gil.fedorapeople.org/randomizedtesting-2.0.9-1.fc19.src.rpm
# com.carrotsearch.randomizedtesting:randomizedtesting-runner:jar:2.0.10 NOT FOUND... unreleased?
# org.apache.lucene:lucene-analyzers-common:jar:4.3.0,
# org.apache.mrunit:mrunit:jar:hadoop1:1.0.0, http://www.apache.org/dist/mrunit/mrunit-1.0.0/apache-mrunit-1.0.0-hadoop2-src.tar.gz
# org.apache.hadoop:hadoop-core:jar:1.1.2:

BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(com.thoughtworks.xstream:xstream)
BuildRequires: mvn(commons-cli:commons-cli)
BuildRequires: mvn(commons-csv:commons-csv)
BuildRequires: mvn(commons-dbcp:commons-dbcp)
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(commons-pool:commons-pool)
BuildRequires: mvn(javax.servlet:servlet-api)
# org.apache.commons:commons-math:jar:2.2
BuildRequires: mvn(org.apache.commons:commons-math3)
# /home/gil/rpmbuild/RPMS/noarch/hsqldb2-2.2.9-1.fc19.noarch.rpm
# BuildRequires: mvn(org.apache.hadoop:hadoop-common)
# BuildRequires: mvn(org.apache.hadoop:hadoop-mapreduce-client-common)
# BuildRequires: mvn(org.apache.hadoop:hadoop-mapreduce-client-core)
BuildRequires: mvn(org.apache.lucene:lucene-analyzers)
BuildRequires: mvn(org.apache.lucene:lucene-benchmark)
BuildRequires: mvn(org.apache.lucene:lucene-core)
# http://gil.fedorapeople.org/apache-commons-cli2-2.0-0.1.SNAPSHOT.20130823.fc19.src.rpm
# http://gil.fedorapeople.org/apache-commons-cli2.spec
BuildRequires: mvn(org.apache.mahout.commons:commons-cli)
BuildRequires: mvn(org.codehaus.jackson:jackson-core-asl)
BuildRequires: mvn(org.codehaus.jackson:jackson-mapper-asl)
BuildRequires: mvn(org.mongodb:bson)
BuildRequires: mvn(org.mongodb:mongo-java-driver)
BuildRequires: mvn(org.slf4j:slf4j-api)
# http://gil.fedorapeople.org/uncommons-antlib-0.3.2-1.fc19.src.rpm
# http://gil.fedorapeople.org/uncommons-antlib.spec
# http://gil.fedorapeople.org/uncommons-maths-1.2.3-1.fc19.src.rpm
# http://gil.fedorapeople.org/uncommons-maths.spec
BuildRequires: mvn(org.uncommons.maths:uncommons-maths)

# test deps
BuildRequires: mvn(commons-codec:commons-codec)
BuildRequires: mvn(commons-configuration:commons-configuration)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.easymock:easymock)
BuildRequires: mvn(org.slf4j:slf4j-jcl)

BuildRequires: apache-resource-bundles
# https://bugzilla.redhat.com/show_bug.cgi?id=1000413
BuildRequires: mahout-collection-codegen-plugin
BuildRequires: maven-antrun-plugin
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-site-plugin
BuildRequires: maven-source-plugin

BuildArch:     noarch

%description
Mahout's goal is to build scalable machine learning libraries.
With scalable we mean: 
Scalable to reasonably large data sets. Our core algorithms for clustering,
classification and batch based collaborative filtering are implemented on top of
Apache Hadoop using the map/reduce paradigm. However we do not restrict
contributions to Hadoop based implementations: Contributions that run on a single
node or on a non-Hadoop cluster are welcome as well. The core libraries are highly
optimized to allow for good performance also for non-distributed algorithms.
The goal of Mahout is to build a vibrant, responsive, diverse
community to facilitate discussions not only on the project itself but also on potential
use cases. Come to the mailing lists to find out more.
Currently Mahout supports mainly four use cases: Recommendation mining takes
users' behavior and from that tries to find items users might like. Clustering takes e.g.
text documents and groups them into groups of topically related documents.
Classification learns from existing categorized documents what documents of a
specific category look like and is able to assign unlabelled documents to the
(hopefully) correct category. Frequent itemset mining takes a set of item groups
(terms in a query session, shopping cart content) and identifies, which individual items
usually appear together.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-distribution-%{version}
find . -name "*.jar" -print -delete
find . -name "*.class" -print -delete

%pom_disable_module buildtools
%pom_disable_module distribution

%pom_xpath_set "pom:project/pom:dependencyManagement/pom:dependencies/pom:dependency[pom:groupId = 'org.apache.commons' ]/pom:artifactId" commons-math3
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'org.apache.commons' ]/pom:artifactId" commons-math3 math
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'org.apache.commons' ]/pom:artifactId" commons-math3 core

%pom_xpath_remove "pom:project/pom:profiles" core

%pom_xpath_inject "pom:project/pom:dependencies" "
<dependency>
 <groupId>org.apache.hadoop</groupId>
 <artifactId>hadoop-common</artifactId>
 <scope>system</scope>
 <systemPath>/home/gil/rpmbuild/BUILD/hadoop-common-b92d9bcf559cc2e62fc166e09bd2852766b27bec/hadoop-common-project/hadoop-common/target/hadoop-common-2.0.5-alpha.jar</systemPath>
</dependency>" core

%pom_xpath_inject "pom:project/pom:dependencies" "
<dependency>
 <groupId>org.apache.hadoop</groupId>
 <artifactId>hadoop-mapreduce-client-core</artifactId>
 <scope>system</scope>
 <systemPath>/home/gil/rpmbuild/BUILD/hadoop-common-b92d9bcf559cc2e62fc166e09bd2852766b27bec/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-core/target/hadoop-mapreduce-client-core-2.0.5-alpha.jar</systemPath>
</dependency>" core

#%%pom_xpath_inject "pom:project/pom:profiles/pom:profile/pom:dependencies/pom:dependency[pom:artifactId = 'hadoop-mapreduce-client-common' ]"

%pom_remove_dep org.apache.hadoop:
# org.apache.commons:commons-math:jar:2.2
sed -i "s|org.apache.commons.math|org.apache.commons.math3|" math/src/main/java/org/apache/mahout/math/ssvd/EigenSolverWrapper.java
sed -i "s|EigenDecompositionImpl|EigenDecomposition|" math/src/main/java/org/apache/mahout/math/ssvd/EigenSolverWrapper.java
sed -i "s|org.apache.commons.math|org.apache.commons.math3|"  \
 core/src/main/java/org/apache/mahout/classifier/sgd/TPrior.java

# require  org.apache.commons.math.ConvergenceException
#          org.apache.commons.math.FunctionEvaluationException
#          org.apache.commons.math.analysis.UnivariateRealFunction
#          org.apache.commons.math.analysis.integration.UnivariateRealIntegrator
rm -r math/src/test/java/org/apache/mahout/math/jet/random/DistributionChecks.java \
 math/src/test/java/org/apache/mahout/math/jet/random/NormalTest.java \
 math/src/test/java/org/apache/mahout/math/jet/random/ExponentialTest.java
# cannot find symbol
#[ERROR] symbol:   method createMockBuilder(java.lang.Class<capture#1 of ?>)
#[ERROR] location: class org.apache.mahout.common.DummyStatusReporter
rm -r core/src/test/java/org/apache/mahout/common/DummyStatusReporter.java \
 core/src/test/java/org/apache/mahout/common/DummyRecordWriter.java \
 core/src/test/java/org/apache/mahout/clustering/canopy/TestCanopyCreation.java \
 core/src/test/java/org/apache/mahout/clustering/meanshift/TestMeanShift.java \
 core/src/test/java/org/apache/mahout/clustering/spectral/common/TestAffinityMatrixInputJob.java \
 core/src/test/java/org/apache/mahout/clustering/spectral/common/TestMatrixDiagonalizeJob.java \
 core/src/test/java/org/apache/mahout/clustering/spectral/common/TestUnitVectorizerJob.java \
 core/src/test/java/org/apache/mahout/clustering/spectral/common/TestVectorMatrixMultiplicationJob.java \
 core/src/test/java/org/apache/mahout/clustering/spectral/eigencuts/TestEigencutsSensitivityJob.java \
 core/src/test/java/org/apache/mahout/clustering/spectral/eigencuts/TestEigencutsAffinityCutsJob.java
# these test fails cause: java.lang.NoClassDefFoundError: Could not initialize class org.apache.hadoop.security.UserGroupInformation
# java.lang.IllegalArgumentException: org.apache.hadoop.mapreduce.Reducer$Context is not an interface
rm -r core/src/test/java/org/apache/mahout/vectorizer/SparseVectorsFromSequenceFilesTest.java \
 core/src/test/java/org/apache/mahout/vectorizer/collocations/llr/CollocMapperTest.java \
 core/src/test/java/org/apache/mahout/vectorizer/collocations/llr/CollocReducerTest.java \
 core/src/test/java/org/apache/mahout/vectorizer/collocations/llr/LLRReducerTest.java \
 core/src/test/java/org/apache/mahout/vectorizer/EncodedVectorsFromSequenceFilesTest.java \
 core/src/test/java/org/apache/mahout/vectorizer/DocumentProcessorTest.java \
 core/src/test/java/org/apache/mahout/fpm/pfpgrowth/FPGrowthTest.java \
 core/src/test/java/org/apache/mahout/math/hadoop/* \
 core/src/test/java/org/apache/mahout/cf/taste/hadoop/* \
 core/src/test/java/org/apache/mahout/math/stats/entropy/ConditionalEntropyTest.java \
 core/src/test/java/org/apache/mahout/math/stats/entropy/EntropyTest.java \
 core/src/test/java/org/apache/mahout/math/stats/entropy/InformationGainTest.java \
 core/src/test/java/org/apache/mahout/math/stats/entropy/InformationGainRatioTest.java \
 core/src/test/java/org/apache/mahout/classifier/naivebayes/NaiveBayesTest.java \
 core/src/test/java/org/apache/mahout/cf/taste/impl/recommender/svd/SVDRecommenderTest.java \
 core/src/test/java/org/apache/mahout/classifier/naivebayes/training/ThetaMapperTest.java \
 core/src/test/java/org/apache/mahout/classifier/naivebayes/training/WeightsMapperTest.java \
 core/src/test/java/org/apache/mahout/classifier/df/data/DataLoaderTest.java \
 core/src/test/java/org/apache/mahout/classifier/df/mapreduce/partial/Step1MapperTest.java \
 core/src/test/java/org/apache/mahout/classifier/df/mapreduce/partial/PartialBuilderTest.java \
 core/src/test/java/org/apache/mahout/clustering/kmeans/TestRandomSeedGenerator.java \
 core/src/test/java/org/apache/mahout/clustering/kmeans/TestKmeansClustering.java \
 core/src/test/java/org/apache/mahout/clustering/classify/ClusterClassificationDriverTest.java \
 core/src/test/java/org/apache/mahout/clustering/lda/cvb/TestCVBModelTrainer.java \
 core/src/test/java/org/apache/mahout/clustering/fuzzykmeans/TestFuzzyKmeansClustering.java \
 core/src/test/java/org/apache/mahout/clustering/minhash/TestMinHashClustering.java \
 core/src/test/java/org/apache/mahout/clustering/topdown/postprocessor/ClusterCountReaderTest.java \
 core/src/test/java/org/apache/mahout/clustering/topdown/postprocessor/ClusterOutputPostProcessorTest.java \
 core/src/test/java/org/apache/mahout/clustering/iterator/TestClusterClassifier.java \
 core/src/test/java/org/apache/mahout/clustering/spectral/common/TestVectorCache.java \
 core/src/test/java/org/apache/mahout/clustering/dirichlet/TestMapReduce.java \
 core/src/test/java/org/apache/mahout/clustering/dirichlet/TestDirichletClustering.java \
 core/src/test/java/org/apache/mahout/vectorizer/HighDFWordsPrunerTest.java \
 core/src/test/java/org/apache/mahout/vectorizer/DictionaryVectorizerTest.java \
 core/src/test/java/org/apache/mahout/fpm/pfpgrowth/PFPGrowthTest.java \
 core/src/test/java/org/apache/mahout/fpm/pfpgrowth/PFPGrowthRetailDataTest.java \
 core/src/test/java/org/apache/mahout/fpm/pfpgrowth/PFPGrowthTest2.java \
 core/src/test/java/org/apache/mahout/classifier/naivebayes/training/IndexInstancesMapperTest.java
 
# java.lang.NoClassDefFoundError: org/apache/commons/codec/binary/Base64
%pom_add_dep commons-codec:commons-codec::test core
#[24,32] cannot find symbol
#[ERROR] symbol:   class DummyRecordWriter
#[ERROR] location: package org.apache.mahout.common
rm -r integration/src/test/java/org/apache/mahout/utils/regex/RegexMapperTest.java \
 integration/src/test/java/org/apache/mahout/clustering/cdbw/TestCDbwEvaluator.java \
 integration/src/test/java/org/apache/mahout/utils/regex/RegexUtilsTest.java \
 integration/src/test/java/org/apache/mahout/clustering/TestClusterEvaluator.java
# java.lang.NoClassDefFoundError: Could not initialize class org.apache.hadoop.security.UserGroupInformation
rm -r integration/src/test/java/org/apache/mahout/clustering/TestClusterDumper.java \
 integration/src/test/java/org/apache/mahout/text/SequenceFilesFromMailArchivesTest.java \
 integration/src/test/java/org/apache/mahout/text/TestSequenceFilesFromDirectory.java \
 integration/src/test/java/org/apache/mahout/utils/SplitInputTest.java \
 integration/src/test/java/org/apache/mahout/utils/vectors/io/VectorWriterTest.java

# java.lang.NoClassDefFoundError: org/apache/commons/configuration/Configuration
%pom_add_dep commons-configuration:commons-configuration::test integration

%pom_add_dep commons-configuration:commons-configuration::test examples

%pom_add_dep commons-cli:commons-cli core
%pom_remove_plugin :maven-assembly-plugin core

%pom_remove_plugin :maven-assembly-plugin examples
%pom_remove_plugin :maven-dependency-plugin examples

%pom_remove_plugin :maven-dependency-plugin integration

# org.apache.solr:solr-commons-csv:jar:3.5.0
# org.mongodb:mongo-java-driver:jar:2.5
# org.mongodb:bson:jar:2.5,
# org.apache.cassandra:cassandra-all:jar:0.8.1
# me.prettyprint:hector-core:jar:0.8.0-2
%pom_remove_dep org.apache.solr:solr-commons-csv integration
%pom_add_dep commons-csv:commons-csv integration
%pom_remove_dep org.apache.cassandra:cassandra-all integration
rm -r integration/src/main/java/org/apache/mahout/cf/taste/impl/model/cassandra/*
%pom_remove_dep me.prettyprint:hector-core integration

%build

%mvn_build
-f -- -Phadoop-0.23
a
%install

%files
#%dir
%{_javadir}/
%{_mavenpomdir}/JPP*.pom
%{_mavendepmapfragdir}/%{name}
#%doc

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Aug 23 2013 gil cattaneo <puntogil@libero.it> 0.7-1
- initial rpm