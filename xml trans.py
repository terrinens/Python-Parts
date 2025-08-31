import xml.etree.ElementTree as ET
import deepl

auth_key = ""
deepl_client = deepl.DeepLClient(auth_key)

def parse_translation_xml():
    """
    XML 파일에서 'text' 태그의 'name'과 'text' 속성 값을 파싱하여 출력합니다.

    Args:
        file_path (str): 파싱할 XML 파일의 경로입니다.
    """
    file_path = "test.xml"
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # <texts> 태그를 찾습니다.
        texts_element = root.find('texts')

        if texts_element is not None:
            
            for text_tag in texts_element.findall('text'):
                name_attr = text_tag.get('name')
                text_attr = text_tag.get('text')
                
                # 'name'과 'text' 속성이 모두 있는지 확인
                if name_attr is not None and text_attr is not None:
                    result = deepl_client.translate_text(text_attr, target_lang="ko")
                    print(f"번역 대상 : {text_attr} => 번역 후 : {result.text}")
                    text_tag.set('text', result.text)
            
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            print("\n파일이 성공적으로 저장되었습니다.")
        else:
            print("XML 파일에 <texts> 태그가 없습니다.")
            
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
    except ET.ParseError:
        print(f"오류: '{file_path}' 파일의 형식이 올바르지 않습니다.")

# 사용 예시
xml_file_path = 'test.xml'  # XML 파일 경로를 여기에 입력하세요.
parse_translation_xml()