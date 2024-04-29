# Author: Nicola D'Ambrosio (nicola.dambrosio2@unina.it)


ARCHITECTURE=$1
ARCHITECTURE_FILE=$ARCHITECTURE".P"
ARCHITECTURE_PATH="$(pwd)/Personnal_simulations/"$ARCHITECTURE_FILE
RULE_SET="Rules_for_OCD.P"
# RULE_SET="interaction_rules_with_metrics.P"
RULE_SET_PATH="$(pwd)/Personnal_simulations/"$RULE_SET 
OUTPUT_DIR="$(pwd)/Personnal_simulations/output_"$ARCHITECTURE

cmd.exe /C taskkill /IM Acrobat.exe /F 2> /dev/null || true
rm -rf $OUTPUT_DIR && mkdir $OUTPUT_DIR

docker run -ti --name mulval -v $OUTPUT_DIR:/input -d --rm wilbercui/mulval bash -c "tail -f /dev/null"
docker cp $ARCHITECTURE_PATH  mulval:/input
docker cp $RULE_SET_PATH mulval:/input

docker exec mulval bash -c "graph_gen.sh  ${ARCHITECTURE_FILE} --cvss -v -r ${RULE_SET}"
docker stop mulval
